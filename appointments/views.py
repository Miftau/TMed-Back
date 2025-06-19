from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from medical_record.models import MedicalRecord
from medical_record.serializers import MedicalRecordSerializer
from .models import Appointment
from .serializers import AppointmentSerializer
from users.models import DoctorProfile
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()


class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def generate_jitsi_url(self):
        room_name = f"medcall-{uuid.uuid4().hex[:8]}"
        return f"https://meet.jit.si/{room_name}"

    def perform_create(self, serializer):
        doctor_id = self.request.data.get('doctor')
        doctor = DoctorProfile.objects.get(id=doctor_id)
        serializer.save(patient=self.request.user, doctor=doctor)
        appointment = serializer.save(patient=self.request.user)
        appointment.video_call_url = self.generate_jitsi_url()
        appointment.save()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class PatientAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)


class DoctorAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(doctor__user=self.request.user)



class PatientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'patient_profile'):
            return Response({"error": "Not a patient"}, status=403)

        upcoming_appointments = Appointment.objects.filter(patient=user).order_by('date')[:5]
        medical_records = MedicalRecord.objects.filter(patient=user).order_by('-created_at')[:3]

        data = {
            "upcoming_appointments": AppointmentSerializer(upcoming_appointments, many=True).data,
            "recent_records": MedicalRecordSerializer(medical_records, many=True).data
        }
        return Response(data)
class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'doctor_profile'):
            return Response({"error": "Not a doctor"}, status=403)

        today_appointments = Appointment.objects.filter(doctor__user=user).order_by('time')[:5]
        recent_patients = MedicalRecord.objects.filter(doctor__user=user).order_by('-created_at')[:5]

        data = {
            "today_appointments": AppointmentSerializer(today_appointments, many=True).data,
            "recent_records": MedicalRecordSerializer(recent_patients, many=True).data
        }
        return Response(data)

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Admin only"}, status=403)

        total_users = User.objects.count()
        total_appointments = Appointment.objects.count()
        total_records = MedicalRecord.objects.count()

        data = {
            "users": total_users,
            "appointments": total_appointments,
            "medical_records": total_records
        }
        return Response(data)




