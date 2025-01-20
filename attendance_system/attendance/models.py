from django.db import models
from django.contrib.auth.models import User
from datetime import date,time


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's built-in User model
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Optional profile picture
    face_encoding = models.BinaryField(blank=True, null=True)  # Optional field for storing face encodings

    def __str__(self):
        # Use the user's email and name for a readable string representation
        return f"{self.user.email} - {self.user.first_name} {self.user.last_name}"



class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)  # Ensures relation to the Student model
    date = models.DateField(default=date.today)  # Defaults to today's date
    time_in = models.TimeField(auto_now_add=True)  # Automatically captures the time when attendance is marked
    status = models.CharField(
        max_length=20, 
        choices=[
            ('present', 'Present'),
            ('absent', 'Absent'),
        ], 
        default='present'
    )

    class Meta:
        unique_together = ['student', 'date']  # Prevents duplicate entries for the same student on the same date
        ordering = ['-date', 'time_in']  # Orders attendance records by date (most recent first) and time

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.date} - {self.status}"

    def mark_present(self):
        """Utility method to mark attendance as present."""
        self.status = 'present'
        self.save()

    def mark_absent(self):
        """Utility method to mark attendance as absent."""
        self.status = 'absent'
        self.save()
