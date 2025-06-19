from django.urls import path
from .views import *
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:id>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctor/availability/', DoctorAvailabilityListCreateView.as_view(), name='availability-list-create'),
    path('doctor/availability/<int:pk>/', DoctorAvailabilityDetailView.as_view(), name='availability-detail'),
    path('doctor/dashboard/', DoctorDashboardView.as_view(), name='doctor-dashboard'),
    path('patient/dashboard/', PatientDashboardView.as_view(), name='patient-dashboard'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
]
