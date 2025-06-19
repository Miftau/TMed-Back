from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"


class PatientProfile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Patient: {self.user.email}"


class DoctorProfile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Doctor: {self.user.email}"

class Availability(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.user.username} - {self.day_of_week} ({self.start_time} to {self.end_time})"



