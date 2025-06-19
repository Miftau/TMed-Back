from django.db import models
from users.models import DoctorProfile, User
from utils.jitsi_token import generate_jitsi_jwt
import uuid


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.TextField(blank=True)
    video_call_url = models.URLField(blank=True, null=True)
    room_name = f"room-{uuid.uuid4().hex[:10]}"

    def generate_video_token(self):
        room_name = f"{self.id}-{self.date}"
        return generate_jitsi_jwt(
            room_name=room_name,
            user_name=self.patient.username,
            user_email=self.patient.email,
            is_moderator=False
        )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.user.username} ({self.date})"

