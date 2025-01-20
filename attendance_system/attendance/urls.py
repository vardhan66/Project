from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.register, name='signup'),  # Signup page
    path('accounts/profile/', views.profile, name='profile'),  # User profile (Django auth system)
    path('dashboard/', views.dashboard, name='dashboard'),  # User dashboard
    # Mark attendance route (this should register the face and mark attendance)
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),  # Mark attendance
    
]
