from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max

# --- USER PROFILE ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)
    instructor_id = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('Admin', 'Admin'), 
        ('Instructor', 'Instructor'), 
        ('Student', 'Student'), 
        ('Analyst', 'Analyst')
    ])

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    def clean(self):
        """
        This runs before saving to ensure data integrity.
        It forces the 'wrong' ID to be None regardless of what the form sent.
        """
        if self.role == 'Student':
            self.instructor_id = None
        elif self.role == 'Instructor':
            self.student_id = None
        elif self.role in ['Admin', 'Analyst']:
            self.student_id = None
            self.instructor_id = None
# --- MAIN ENTITIES ---

class University(models.Model):
    university_id = models.IntegerField(primary_key=True)
    university_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.university_name

    class Meta:
        managed = True
        db_table = 'university'

class Instructor(models.Model):
    instructor_id = models.IntegerField(primary_key=True)
    instructor_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True)
    years_experience = models.IntegerField(blank=True, null=True)
    expertise = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.instructor_name

    class Meta:
        managed = True
        db_table = 'instructor'

class Topic(models.Model):
    topic_id = models.IntegerField(primary_key=True)
    topic_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.topic_name

    class Meta:
        managed = True
        db_table = 'topic'

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    # university removed to prevent column errors (handled in CourseUniversity)
    course_name = models.CharField(max_length=100)
    duration_months = models.IntegerField(blank=True, null=True)
    program_type = models.CharField(max_length=50, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.course_name

    class Meta:
        managed = True
        db_table = 'course'

class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.student_name

    class Meta:
        managed = True
        db_table = 'student'

class Textbook(models.Model):
    isbn_number = models.CharField(primary_key=True, max_length=20)
    author = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title or self.isbn_number

    class Meta:
        managed = True
        db_table = 'textbook'

class OnlineContent(models.Model):
    content_id = models.IntegerField(primary_key=True)
    content_type = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title or f'Content {self.content_id}'

    class Meta:
        managed = True
        db_table = 'online_content'

class Evaluation(models.Model):
    evaluation_id = models.IntegerField(primary_key=True)
    student = models.ForeignKey('Student', models.DO_NOTHING, blank=True, null=True, db_column='student_id')
    course = models.ForeignKey('Course', models.DO_NOTHING, blank=True, null=True, db_column='course_id')
    marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'evaluation'

# --- JUNCTION TABLES ---
# Using Django's default auto-increment 'id' as PK with unique_together
# for composite uniqueness. This allows proper many-to-many relationships.

class CourseContent(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, db_column='course_id')
    content = models.ForeignKey(OnlineContent, models.CASCADE, db_column='content_id')

    class Meta:
        managed = True
        db_table = 'course_content'
        unique_together = (('course', 'content'),)

class CourseInstructor(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, db_column='course_id')
    instructor = models.ForeignKey(Instructor, models.CASCADE, db_column='instructor_id')

    class Meta:
        managed = True
        db_table = 'course_instructor'
        unique_together = (('course', 'instructor'),)

class CourseTextbook(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, db_column='course_id')
    isbn_number = models.ForeignKey(Textbook, models.CASCADE, db_column='isbn_number')

    class Meta:
        managed = True
        db_table = 'course_textbook'
        unique_together = (('course', 'isbn_number'),)

class CourseTopic(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, db_column='course_id')
    topic = models.ForeignKey(Topic, models.CASCADE, db_column='topic_id')

    class Meta:
        managed = True
        db_table = 'course_topic'
        unique_together = (('course', 'topic'),)

class CourseUniversity(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, db_column='course_id')
    university = models.ForeignKey(University, models.CASCADE, db_column='university_id')

    class Meta:
        managed = True
        db_table = 'course_university'
        unique_together = (('course', 'university'),)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, models.CASCADE, db_column='student_id')
    course = models.ForeignKey(Course, models.CASCADE, db_column='course_id')
    enrollment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'enrollment'
        unique_together = (('student', 'course'),)

# --- AUTOMATION SIGNALS ---
# This code runs automatically when a new user Profile is created.
# It creates the corresponding Student or Instructor row in the database
# and links the ID back to the profile.

@receiver(post_save, sender=Profile)
def auto_create_student_or_instructor(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'Student':
            # 1. Calculate next Student ID
            max_id = Student.objects.aggregate(Max('student_id'))['student_id__max']
            new_id = 1 if max_id is None else max_id + 1
            
            # 2. Create the Student row
            Student.objects.create(
                student_id=new_id,
                student_name=instance.user.username,
                email=instance.user.email,
                age=20,       # Default
                country='India', # Default
                category='General' # Default
            )
            
            # 3. Link back to Profile
            instance.student_id = new_id
            instance.save()

        elif instance.role == 'Instructor':
            # 1. Calculate next Instructor ID
            max_id = Instructor.objects.aggregate(Max('instructor_id'))['instructor_id__max']
            new_id = 1 if max_id is None else max_id + 1
            
            # 2. Create the Instructor row
            Instructor.objects.create(
                instructor_id=new_id,
                instructor_name=instance.user.username,
                email=instance.user.email,
                years_experience=0,
                expertise='Pending'
            )
            
            # 3. Link back to Profile
            instance.instructor_id = new_id
            instance.save()