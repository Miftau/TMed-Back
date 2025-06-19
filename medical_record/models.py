from django.db import models
from django.contrib.auth import get_user_model
from users.models import DoctorProfile

User = get_user_model()

class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True)
    condition = models.CharField(max_length=255)
    notes = models.TextField()
    prescriptions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.condition} ({self.created_at.date()})"

class RecordAccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} accessed {self.record} at {self.timestamp}"




