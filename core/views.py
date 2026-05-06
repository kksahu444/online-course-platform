from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from django.db.models import Max, Count, Avg
# IMPORTS UPDATED HERE:
from .forms import AddContentForm, AssignInstructorForm, SignupForm
from .models import (
    Course, OnlineContent, CourseContent, Enrollment, 
    Evaluation, CourseInstructor, Instructor, Profile
)
import datetime
import json

# --- NEW: Signup View ---
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']

            # Create the Profile (This triggers your Signals in models.py to auto-create Student/Instructor rows)
            Profile.objects.create(user=user, role=role)

            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

# --- YOUR EXISTING VIEWS BELOW (No changes needed) ---

@login_required
def dashboard_redirect(request):
    # Your existing logic...
    try:
        role = request.user.profile.role
    except:
        return redirect('login') # Safety catch

    if role == 'Admin':
        return render(request, 'dashboards/admin.html')
    elif role == 'Instructor':
        inst_id = request.user.profile.instructor_id
        has_assigned_courses = False
        if inst_id:
            has_assigned_courses = CourseInstructor.objects.filter(instructor_id=inst_id).exists()
        context = {'has_assigned_courses': has_assigned_courses}
        return render(request, 'dashboards/instructor.html', context)
    elif role == 'Student':
        return render(request, 'dashboards/student.html')
    elif role == 'Analyst':
        return render(request, 'dashboards/analyst.html')
    return redirect('login')

@login_required
def course_list(request):
    # Your existing logic...
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(course_name__icontains=query)
    else:
        courses = Course.objects.all()
    return render(request, 'student/course_list.html', {'courses': courses})

@login_required
def register_course(request, course_id):
    # Your existing logic...
    if request.method == 'POST':
        try:
            student_id = request.user.profile.student_id
            if not student_id:
                messages.error(request, "Error: No Student ID linked to your account.")
                return redirect('course_list')
        except:
            messages.error(request, "Profile error. Please contact Admin.")
            return redirect('course_list')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Enrollment WHERE student_id = %s AND course_id = %s", [student_id, course_id])
            row = cursor.fetchone()
            if row:
                messages.warning(request, "You are already enrolled in this course!")
            else:
                current_date = datetime.date.today()
                cursor.execute(
                    "INSERT INTO Enrollment (student_id, course_id, enrollment_date, status) VALUES (%s, %s, %s, %s)",
                    [student_id, course_id, current_date, 'Enrolled']
                )
                messages.success(request, f"Successfully registered for Course ID {course_id}!")
    return redirect('course_list')

@login_required
def add_content(request):
    # Your existing logic...
    if request.user.profile.role != 'Instructor':
        messages.error(request, "Access Denied: Instructor privileges required.")
        return redirect('dashboard')

    inst_id = request.user.profile.instructor_id
    has_assigned_courses = CourseInstructor.objects.filter(instructor_id=inst_id).exists()

    if request.method == 'POST':
        form = AddContentForm(request.POST, instructor_id=inst_id)
        if form.is_valid():
            try:
                max_id = OnlineContent.objects.aggregate(Max('content_id'))['content_id__max']
                new_id = 1 if max_id is None else max_id + 1
                
                content = form.save(commit=False)
                content.content_id = new_id
                content.save()
                
                selected_course = form.cleaned_data['course']
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Course_Content (course_id, content_id) VALUES (%s, %s)",
                        [selected_course.course_id, content.content_id]
                    )
                messages.success(request, f"Added '{content.title}' to {selected_course.course_name}!")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Database Error: {str(e)}")
    else:
        form = AddContentForm(instructor_id=inst_id)

    return render(request, 'instructor/add_content.html', {
        'form': form,
        'has_assigned_courses': has_assigned_courses
    })

@login_required
def analyst_dashboard(request):
    if request.user.profile.role != 'Analyst':
        messages.error(request, "Access Denied: Data Analyst privileges required.")
        return redirect('dashboard')

    courses = Course.objects.all()
    stats = None
    selected_course_id = request.GET.get('course')

    if selected_course_id:
        try:
            selected_course = Course.objects.get(course_id=selected_course_id)
            enrollment_count = Enrollment.objects.filter(course=selected_course).count()
            avg_marks_result = Evaluation.objects.filter(course=selected_course).aggregate(Avg('marks'))
            avg_marks = avg_marks_result['marks__avg']
            stats = {
                'course': selected_course,
                'enrollment_count': enrollment_count,
                'avg_marks': round(float(avg_marks), 2) if avg_marks else 'N/A',
            }
        except Course.DoesNotExist:
            pass

    # Chart data for all courses
    enrollment_qs = Course.objects.annotate(student_count=Count('enrollment'))
    labels = [c.course_name for c in enrollment_qs]
    counts = [c.student_count for c in enrollment_qs]

    return render(request, 'dashboards/analyst.html', {
        'courses': courses,
        'stats': stats,
        'labels': labels,
        'counts': counts,
    })

@login_required
def assign_instructor(request):
    # Your existing logic...
    if request.user.profile.role != 'Admin':
        messages.error(request, "Access Denied: System Admin privileges required.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = AssignInstructorForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            instructor = form.cleaned_data['instructor']
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM Course_Instructor WHERE course_id = %s AND instructor_id = %s", [course.course_id, instructor.instructor_id])
                    if cursor.fetchone():
                        messages.warning(request, f"{instructor.instructor_name} is already assigned to {course.course_name}.")
                    else:
                        cursor.execute("INSERT INTO Course_Instructor (course_id, instructor_id) VALUES (%s, %s)", [course.course_id, instructor.instructor_id])
                        messages.success(request, f"Successfully assigned {instructor.instructor_name} to {course.course_name}!")
                        return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Database Error: {str(e)}")
    else:
        form = AssignInstructorForm()
    return render(request, 'admin/assign_instructor.html', {'form': form})