"""
Seed script to populate the database with sample data for testing.
Run: python seed_data.py

IMPORTANT: This script disconnects the post_save signal temporarily
to prevent the auto-creation of duplicate Student/Instructor rows.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_platform.settings')
django.setup()

from django.contrib.auth.models import User
from django.db.models import Max
from django.db.models.signals import post_save
from core.models import (
    Profile, University, Instructor, Topic, Course, Student,
    Textbook, OnlineContent, CourseUniversity, CourseInstructor,
    CourseTopic, CourseContent, Enrollment, Evaluation,
    auto_create_student_or_instructor  # the signal handler
)
import datetime

# --- DISCONNECT the signal to prevent duplicate rows ---
post_save.disconnect(auto_create_student_or_instructor, sender=Profile)

print("=== Seeding Database ===")

# --- 1. Universities ---
universities = [
    (1, 'IIT Kharagpur', 'India'),
    (2, 'Stanford University', 'USA'),
    (3, 'MIT', 'USA'),
    (4, 'University of Oxford', 'UK'),
]
for uid, name, country in universities:
    University.objects.get_or_create(university_id=uid, defaults={'university_name': name, 'country': country})
print(f"  Universities: {University.objects.count()}")

# --- 2. Topics ---
topics = [
    (1, 'Machine Learning', 'Computer Science'),
    (2, 'Database Systems', 'Computer Science'),
    (3, 'Web Development', 'Computer Science'),
    (4, 'Data Structures', 'Computer Science'),
    (5, 'Artificial Intelligence', 'Computer Science'),
]
for tid, name, cat in topics:
    Topic.objects.get_or_create(topic_id=tid, defaults={'topic_name': name, 'category': cat})
print(f"  Topics: {Topic.objects.count()}")

# --- 3. Courses ---
courses = [
    (1, 'Introduction to Machine Learning', 3, 'Certificate', 4.5),
    (2, 'Advanced Database Management', 4, 'Diploma', 4.2),
    (3, 'Full Stack Web Development', 6, 'Certificate', 4.8),
    (4, 'Data Structures & Algorithms', 3, 'Certificate', 4.6),
    (5, 'Deep Learning Specialization', 5, 'Diploma', 4.9),
]
for cid, name, dur, ptype, rating in courses:
    Course.objects.get_or_create(course_id=cid, defaults={
        'course_name': name, 'duration_months': dur,
        'program_type': ptype, 'rating': rating
    })
print(f"  Courses: {Course.objects.count()}")

# --- 4. Instructors ---
instructors = [
    (1, 'Prof. Sharma', 'sharma@kgp.edu', 10, 'Machine Learning'),
    (2, 'Prof. Das', 'das@kgp.edu', 8, 'Databases'),
]
for iid, name, email, yrs, exp in instructors:
    Instructor.objects.get_or_create(instructor_id=iid, defaults={
        'instructor_name': name, 'email': email,
        'years_experience': yrs, 'expertise': exp
    })
print(f"  Instructors: {Instructor.objects.count()}")

# --- 5. Students ---
students_data = [
    (1, 'Ritabrata Sarkar', 21, 'India', 'UG', 'ritabrata@kgp.edu'),
    (2, 'Akshat Priyadarshi', 21, 'India', 'UG', 'akshat@kgp.edu'),
    (3, 'Krishnkant Sahu', 20, 'India', 'UG', 'krishnkant@kgp.edu'),
]
for sid, name, age, country, cat, email in students_data:
    Student.objects.get_or_create(student_id=sid, defaults={
        'student_name': name, 'age': age, 'country': country,
        'category': cat, 'email': email
    })
print(f"  Students: {Student.objects.count()}")

# --- 6. Django Users + Profiles (signal is disconnected, so we link IDs manually) ---

# Admin
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@kgp.edu', 'admin123')
    Profile.objects.create(user=admin_user, role='Admin')
    print("  Created: admin / admin123 (Admin)")

# Instructors — link to instructor_id 1 and 2
for uname, email, iid in [('prof_sharma', 'sharma@kgp.edu', 1), ('prof_das', 'das@kgp.edu', 2)]:
    if not User.objects.filter(username=uname).exists():
        user = User.objects.create_user(uname, email, 'pass1234')
        Profile.objects.create(user=user, role='Instructor', instructor_id=iid)
        print(f"  Created: {uname} / pass1234 (Instructor, inst_id={iid})")

# Students — link to student_id 1, 2, 3
for uname, email, sid in [('ritabrata', 'ritabrata@kgp.edu', 1), ('akshat', 'akshat@kgp.edu', 2), ('krishnkant', 'krishnkant@kgp.edu', 3)]:
    if not User.objects.filter(username=uname).exists():
        user = User.objects.create_user(uname, email, 'pass1234')
        Profile.objects.create(user=user, role='Student', student_id=sid)
        print(f"  Created: {uname} / pass1234 (Student, stu_id={sid})")

# Analyst
if not User.objects.filter(username='analyst').exists():
    analyst_user = User.objects.create_user('analyst', 'analyst@kgp.edu', 'pass1234')
    Profile.objects.create(user=analyst_user, role='Analyst')
    print("  Created: analyst / pass1234 (Analyst)")

# --- 7. Junction Tables ---

# Course-University
for cid, uid in [(1, 1), (2, 1), (3, 2), (4, 3), (5, 2)]:
    CourseUniversity.objects.get_or_create(
        course=Course.objects.get(course_id=cid),
        university=University.objects.get(university_id=uid)
    )
print(f"  Course-University: {CourseUniversity.objects.count()}")

# Course-Instructor (prof_sharma=1 gets courses 1,3,5; prof_das=2 gets courses 2,4)
for cid, iid in [(1, 1), (2, 2), (3, 1), (4, 2), (5, 1)]:
    CourseInstructor.objects.get_or_create(
        course=Course.objects.get(course_id=cid),
        instructor=Instructor.objects.get(instructor_id=iid)
    )
print(f"  Course-Instructor: {CourseInstructor.objects.count()}")

# Course-Topic
for cid, tid in [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]:
    CourseTopic.objects.get_or_create(
        course=Course.objects.get(course_id=cid),
        topic=Topic.objects.get(topic_id=tid)
    )
print(f"  Course-Topic: {CourseTopic.objects.count()}")

# --- 8. Enrollments ---
for sid, cid in [(1, 1), (1, 3), (2, 1), (2, 2), (3, 5), (3, 1)]:
    Enrollment.objects.get_or_create(
        student=Student.objects.get(student_id=sid),
        course=Course.objects.get(course_id=cid),
        defaults={'enrollment_date': datetime.date.today(), 'status': 'Enrolled'}
    )
print(f"  Enrollments: {Enrollment.objects.count()}")

# --- 9. Evaluations ---
eval_id = (Evaluation.objects.aggregate(Max('evaluation_id'))['evaluation_id__max'] or 0) + 1
for sid, cid, marks, fb in [(1, 1, 85.5, 'Good work'), (2, 1, 92.0, 'Excellent'), (2, 2, 78.0, 'Needs improvement')]:
    s = Student.objects.get(student_id=sid)
    c = Course.objects.get(course_id=cid)
    if not Evaluation.objects.filter(student=s, course=c).exists():
        Evaluation.objects.create(evaluation_id=eval_id, student=s, course=c, marks=marks, feedback=fb)
        eval_id += 1
print(f"  Evaluations: {Evaluation.objects.count()}")

# --- 10. Online Content ---
for cntid, ctype, title, url in [
    (1, 'Video', 'Intro to ML - Lecture 1', 'https://example.com/ml-lecture1'),
    (2, 'PDF', 'SQL Fundamentals Guide', 'https://example.com/sql-guide.pdf'),
    (3, 'Video', 'React Crash Course', 'https://example.com/react-crash'),
]:
    oc, _ = OnlineContent.objects.get_or_create(content_id=cntid, defaults={
        'content_type': ctype, 'title': title, 'url': url
    })
    CourseContent.objects.get_or_create(
        course=Course.objects.get(course_id=cntid), content=oc
    )
print(f"  OnlineContent: {OnlineContent.objects.count()}")

# --- RECONNECT the signal ---
post_save.connect(auto_create_student_or_instructor, sender=Profile)

# --- Verify data integrity ---
print("\n=== Verification ===")
for p in Profile.objects.filter(role='Instructor'):
    has_courses = CourseInstructor.objects.filter(instructor_id=p.instructor_id).exists()
    print(f"  {p.user.username}: inst_id={p.instructor_id}, has_courses={has_courses}")
for p in Profile.objects.filter(role='Student'):
    enrollments = Enrollment.objects.filter(student_id=p.student_id).count()
    print(f"  {p.user.username}: stu_id={p.student_id}, enrollments={enrollments}")

print("\n=== Seeding Complete! ===")
print(f"  Total Users: {User.objects.count()}")
print(f"  Total Courses: {Course.objects.count()}")
print(f"  Total Enrollments: {Enrollment.objects.count()}")
print("\n  Login Credentials:")
print("  admin       / admin123  (System Admin)")
print("  prof_sharma / pass1234  (Instructor - courses 1,3,5)")
print("  prof_das    / pass1234  (Instructor - courses 2,4)")
print("  ritabrata   / pass1234  (Student)")
print("  akshat      / pass1234  (Student)")
print("  krishnkant  / pass1234  (Student)")
print("  analyst     / pass1234  (Data Analyst)")
