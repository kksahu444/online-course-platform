from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views
from django.views.generic.base import RedirectView

urlpatterns = [
    # 1. Root Redirect
    path('', RedirectView.as_view(url='login/', permanent=False)),

    # 2. CUSTOM Admin Paths
    path('admin/assign-instructor/', views.assign_instructor, name='assign_instructor'),

    # 3. Default Django Admin
    path('admin/', admin.site.urls),

    # 4. Authentication (ADDED SIGNUP HERE)
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),

    # 5. Student Module
    path('courses/', views.course_list, name='course_list'),
    path('register/<int:course_id>/', views.register_course, name='register_course'),

    # 6. Instructor Module
    path('instructor/add-content/', views.add_content, name='add_content'),

    # 7. Analyst Module
    path('analyst/statistics/', views.analyst_dashboard, name='analyst_stats'),
]