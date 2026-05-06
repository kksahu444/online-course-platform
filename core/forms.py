from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, OnlineContent, Instructor

# --- NEW: Signup Form (From Friend) ---
class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Instructor', 'Instructor'),
        ('Analyst', 'Analyst'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# --- YOUR EXISTING: Instructor Form (With Dynamic Filtering) ---
class AddContentForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(), 
        label="Select Course",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        instructor_id = kwargs.pop('instructor_id', None)
        super(AddContentForm, self).__init__(*args, **kwargs)
        if instructor_id:
            self.fields['course'].queryset = Course.objects.filter(
                courseinstructor__instructor_id=instructor_id
            )

    class Meta:
        model = OnlineContent
        fields = ['title', 'content_type', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Lecture 1: Intro to SQL'}),
            'content_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., PDF, Video, Link'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/material'}),
        }

# --- YOUR EXISTING: Admin Form ---
class AssignInstructorForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label="Select Course",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.all(),
        label="Select Instructor",
        widget=forms.Select(attrs={'class': 'form-select'})
    )