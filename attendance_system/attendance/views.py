from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login as auth_login
from django.http import JsonResponse
from .forms import Registerform
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Student, Attendance
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
import face_recognition
import numpy as np
import cv2
import base64
import json
import re
from io import BytesIO
from datetime import date


def home(request):
    return render(request, 'liveness_home.html') 

 # Assuming Student model is in the same app

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use username for login
        email = request.POST.get('email')  # Keep email as a normal field
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        # Check if passwords match
        if password != confirm_password:
            return render(request, 'registration/signup.html', {
                'error': 'Passwords do not match!'
            })
        # Check if all fields are provided
        if not username or not email or not password:
            return render(request, 'registration/signup.html', {
                'error': 'All fields are required!'
            })
        # Create the user object (username for login, email as normal)
        user = User.objects.create_user(username=username, password=password, email=email)
        student = Student(user=user)
        student.save() 
        # Log in the user after successful signup
        auth_login(request, user)
        # Redirect to the profile or dashboard page
        return render(request,'signin.html')  

    return render(request, 'registration/signup.html')


from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use 'username' for login
        password = request.POST.get('password')

        # Authenticate the user by username instead of email
        try:
            user = authenticate(request, username=username, password=password)  # Authenticate using username
            if user is not None:
                auth_login(request, user)
                return redirect('profile')  # Redirect to profile page after successful login
            else:
                return render(request, 'signin.html', {"error": "Invalid username or password"})
        except Exception as e:
            return render(request, 'signin.html', {"error": str(e)})

    return render(request, 'signin.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('profile') 

    return render(request, 'dashboard.html', {'student': student})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def mark_attendance(request):
    student = Student.objects.get(user=request.user)

    # Process the action sent from the frontend
    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data.get('image')
        action = data.get('action')

        # Clean the base64 data (remove data URL part)
        image_data = re.sub('^data:image/.+;base64,', '', image_data)

        # Decode the base64 image
        img_bytes = base64.b64decode(image_data)
        image = np.array(bytearray(img_bytes), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # If registering the face
        if action == 'register':
            # Detect face in the captured image
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) > 0:
                face_encoding = face_recognition.face_encodings(image, face_locations)[0]
                student.face_encoding = np.array(face_encoding).tobytes()  # Save encoding as binary data
                student.save()
                return JsonResponse({'status': 'Face registered successfully'})

            return JsonResponse({'status': 'No face detected'})

        # If marking attendance
        if action == 'mark':
            # Detect face in the captured image
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) > 0:
                face_encoding = face_recognition.face_encodings(image, face_locations)[0]
                stored_encoding = np.frombuffer(student.face_encoding, dtype=np.float64)

                # Compare the captured face with the registered face
                matches = face_recognition.compare_faces([stored_encoding], face_encoding)
                if matches[0]:
                    # Get or create the attendance for the current day
                    attendance, created = Attendance.objects.get_or_create(student=student, date=date.today())
                    if created:
                        # Mark attendance as 'present' when it's newly created
                        attendance.mark_present()
                        return JsonResponse({'status': 'Attendance marked successfully'})
                    else:
                        return JsonResponse({'status': 'Attendance already marked for today'})
                else:
                    return JsonResponse({'status': 'Face not recognized'})
            else:
                return JsonResponse({'status': 'No face detected'})

    return JsonResponse({'status': 'Invalid request'})
