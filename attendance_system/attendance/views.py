from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .forms import Registerform
from .models import Student, Attendance
from django.contrib.auth.decorators import login_required
import face_recognition
import numpy as np
import cv2
from datetime import date

# Register view (Handles user registration)
def register(request):
    if request.method == 'POST':
        form = Registerform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            # Create a new student object after registration
            Student.objects.create(user=user)
            return redirect('login')  # Redirect to the dashboard after registration
    else:
        form = Registerform()
    return render(request, 'registration/register.html', {"form": form})

# Profile view (User profile page)
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

# Dashboard view (Shows user information)
@login_required
def dashboard(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'attendance/dashboard.html', {'student': student})

# Mark attendance view (Handles face registration and attendance marking)
@login_required
def mark_attendance(request):
    student = Student.objects.get(user=request.user)
    
    # Check if the student has already registered their face
    if student.face_encoding:
        # If face is already registered, allow them to mark attendance
        if request.method == 'POST':
            # Mark attendance for the current day
            attendance, created = Attendance.objects.get_or_create(student=student, date=date.today())
            if created:
                attendance.status = 'present'
                attendance.save()
                return JsonResponse({'status': 'Attendance marked successfully'})
            else:
                return JsonResponse({'status': 'Attendance already marked for today'})
        
        return render(request, 'attendance/mark_attendance.html', {'student': student, 'face_registered': True})

    else:
        # If face is not registered, allow the user to register their face
        if request.method == 'POST':
            # Get face image from the form
            face_image = request.FILES['face_image']  # Assuming face image is uploaded through a form
            image = cv2.imread(face_image.path)  # Read the image file
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) > 0:
                # Get face encoding
                face_encoding = face_recognition.face_encodings(image, face_locations)[0]
                student.face_encoding = np.array(face_encoding).tobytes()  # Save encoding as binary data
                student.save()
                return JsonResponse({'status': 'Face registered successfully'})
            else:
                return JsonResponse({'status': 'No face detected in the image'})
        
        return render(request, 'attendance/mark_attendance.html', {'student': student, 'face_registered': False})
