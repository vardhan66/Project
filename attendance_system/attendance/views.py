from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .forms import Registerform
from .models import Student, Attendance
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
    return render(request, 'base.html') 
from django.core.exceptions import ValidationError

def register(request):
    if request.method == 'POST':
        form = Registerform(request.POST)
        if form.is_valid():
            user = form.save()
            student = Student(User=user)
            student.save() 
            login(request, user)
            return redirect('profile')
        form = Registerform()

    return render(request, 'registration/register.html', {"form": form})




@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('profile') 

    return render(request, 'attendance/dashboard.html', {'student': student})

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
                    # Mark attendance for the current day
                    attendance, created = Attendance.objects.get_or_create(student=student, date=date.today())
                    if created:
                        attendance.status = 'present'
                        attendance.save()
                        return JsonResponse({'status': 'Attendance marked successfully'})
                    else:
                        return JsonResponse({'status': 'Attendance already marked for today'})
                else:
                    return JsonResponse({'status': 'Face not recognized'})
            else:
                return JsonResponse({'status': 'No face detected'})

    return JsonResponse({'status': 'Invalid request'})