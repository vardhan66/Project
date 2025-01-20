from django.urls import path
from . import views
import django.contrib.auth.views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.register, name='signup'), 
    path('login/', views.user_login, name='login'),
    path('accounts/profile/', views.profile, name='profile'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('mark-attendance/', views.mark_attendance, name='mark-attendance'), 
    path('logout/', views.logout_view, name='logout'), 
    
]
