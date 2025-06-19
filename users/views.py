from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import *
from .models import *
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializer import CustomTokenObtainPairSerializer
from medical_record.models import MedicalRecord
from medical_record.serializers import MedicalRecordSerializer
from datetime import date


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class DoctorListView(generics.ListAPIView):
    queryset = DoctorProfile.objects.select_related('user').all()
    serializer_class = DoctorDirectorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'specialty', 'location']

class DoctorDetailView(generics.RetrieveAPIView):
    queryset = DoctorProfile.objects.select_related('user').all()
    serializer_class = DoctorDirectorySerializer
    lookup_field = 'id'

class DoctorAvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Availability.objects.filter(doctor__user=self.request.user)

    def perform_create(self, serializer):
        doctor_profile = DoctorProfile.objects.get(user=self.request.user)
        serializer.save(doctor=doctor_profile)

class DoctorAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Availability.objects.filter(doctor__user=self.request.user)


class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            doctor_profile = DoctorProfile.objects.get(user=user)
        except DoctorProfile.DoesNotExist:
            return Response({"error": "Doctor profile not found."}, status=404)

        # Appointments from today onward
        upcoming_appointments = Appointment.objects.filter(
            doctor=doctor_profile,
            date__gte=date.today(),
            status__in=['pending', 'confirmed']
        ).order_by('date', 'start_time')

        # Availability slots
        availability = Availability.objects.filter(doctor=doctor_profile)

        # Optional: get distinct patients seen before
        seen_patients = Appointment.objects.filter(
            doctor=doctor_profile
        ).values('patient__id', 'patient__username').distinct()

        return Response({
            "doctor_profile": DoctorDirectorySerializer(doctor_profile).data,
            "upcoming_appointments": AppointmentSerializer(upcoming_appointments, many=True).data,
            "availability": AvailabilitySerializer(availability, many=True).data,
            "recent_patients": seen_patients
        })


class PatientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Upcoming Appointments
        upcoming_appointments = Appointment.objects.filter(
            patient=user,
            date__gte=date.today(),
            status__in=['pending', 'confirmed']
        ).order_by('date', 'start_time')

        # Medical Records (optional)
        medical_records = MedicalRecord.objects.filter(patient=user) if hasattr(request.user, 'medicalrecord_set') else []

        # Recent Doctors
        recent_doctors = Appointment.objects.filter(
            patient=user
        ).values('doctor__id', 'doctor__user__username', 'doctor__specialty').distinct()

        return Response({
            "profile": UserSerializer(user).data,
            "upcoming_appointments": AppointmentSerializer(upcoming_appointments, many=True).data,
            "medical_records": MedicalRecordSerializer(medical_records, many=True).data if medical_records else [],
            "recent_doctors": recent_doctors
        })

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        User = get_user_model()

        # User stats
        total_users = User.objects.count()
        total_doctors = DoctorProfile.objects.count()
        total_patients = total_users - total_doctors

        # Appointment stats
        total_appointments = Appointment.objects.count()
        pending_appointments = Appointment.objects.filter(status='pending').count()
        confirmed_appointments = Appointment.objects.filter(status='confirmed').count()
        cancelled_appointments = Appointment.objects.filter(status='cancelled').count()
        completed_appointments = Appointment.objects.filter(status='completed').count()

        # Today’s appointments
        from datetime import date
        today_appointments = Appointment.objects.filter(date=date.today()).count()

        return Response({
            "users": {
                "total": total_users,
                "doctors": total_doctors,
                "patients": total_patients
            },
            "appointments": {
                "total": total_appointments,
                "pending": pending_appointments,
                "confirmed": confirmed_appointments,
                "cancelled": cancelled_appointments,
                "completed": completed_appointments,
                "today": today_appointments
            },
            "system_status": "OK"
        })





