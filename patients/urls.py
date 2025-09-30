# patients/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'), # List all patients
    path('create/', views.patient_create, name='patient_create'), # Create new patient
    path('<int:patient_id>/', views.patient_detail, name='patient_detail'), # View patient details
    path('<int:patient_id>/edit/', views.patient_update, name='patient_update'), # Update patient
    path('<int:patient_id>/delete/', views.patient_delete, name='patient_delete'), # Delete patient
]
