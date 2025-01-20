from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    face_encoding = models.BinaryField(blank=True, null=True) 

    def __str__(self):
        return f"{self.roll_number} - {self.user.first_name} {self.user.last_name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    time_in = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent')
    ], default='present')

    class Meta:
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student.user.first_name} - {self.date} - {self.status}"
