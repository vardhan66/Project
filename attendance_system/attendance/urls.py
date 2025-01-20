from django.urls import path
from . import views
import django.contrib.auth.views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.register, name='signup'),  # Signup page
    path('accounts/profile/', views.profile, name='profile'),  # User profile (Django auth system)
    path('dashboard/', views.dashboard, name='dashboard'),  # User dashboard
    # Mark attendance route (this should register the face and mark attendance)
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),  # Mark attendance
    
]
