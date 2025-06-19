from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import MedicalRecordSerializer
from users.models import DoctorProfile
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

class MedicalRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor_profile'):
            records = MedicalRecord.objects.all()
        else:
            records = MedicalRecord.objects.filter(patient=user)

        # Audit log every access
        for record in records:
            RecordAccessLog.objects.create(user=user, record=record)

        return records

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'doctor_profile'):
            doctor_profile = DoctorProfile.objects.get(user=user)
            serializer.save(doctor=doctor_profile)
        else:
            raise PermissionDenied("Only doctors can create medical records.")


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'doctor_profile')

class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def perform_update(self, serializer):
        if not hasattr(self.request.user, 'doctor_profile'):
            raise PermissionDenied("Only doctors can update records.")
        serializer.save()

    def perform_destroy(self, instance):
        if not hasattr(self.request.user, 'doctor_profile'):
            raise PermissionDenied("Only doctors can delete records.")
        instance.delete()

class ExportMedicalRecordPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            record = MedicalRecord.objects.get(pk=pk)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Record not found"}, status=404)

        if request.user != record.patient and not hasattr(request.user, 'doctor_profile'):
            return Response({"error": "Access denied"}, status=403)

        html_string = render_to_string('medical/record_pdf.html', {'record': record})
        pdf = weasyprint.HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="medical_record_{record.id}.pdf"'
        return response

