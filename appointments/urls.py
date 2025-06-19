from django.urls import path
from .views import *
urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='create-appointment'),
    path('patient/', PatientAppointmentListView.as_view(), name='patient-appointments'),
    path('doctor/', DoctorAppointmentListView.as_view(), name='doctor-appointments'),
    path('dashboard/patient/', PatientDashboardView.as_view(), name='patient-dashboard'),
    path('dashboard/doctor/', DoctorDashboardView.as_view(), name='doctor-dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
]