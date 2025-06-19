from django.urls import path
from .views import *

urlpatterns = [
    path('records/', MedicalRecordListCreateView.as_view(), name='medical-records'),
    path('records/<int:pk>/', MedicalRecordDetailView.as_view(), name='record-detail'),
    path('records/<int:pk>/export/', ExportMedicalRecordPDFView.as_view(), name='record-export'),
]
