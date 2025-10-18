# patients/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.add_patient, name='add_patient'),
    path('record_vitals/<int:patient_id>/', views.record_vitals, name='record_vitals'),
    path('patients/<int:patient_id>/vitals/', views.patient_vitals, name='patient_vitals'),
    path('patients/vitals/', views.all_patients_vitals, name='all_patients_vitals'),
    path('add-to-queue/<int:patient_id>/', views.add_patient_to_queue, name='add_patient_to_queue'),
    path('<int:pk>/edit/', views.edit_patient, name='edit_patient'),
    path('<int:pk>/delete/', views.delete_patient, name='delete_patient'),

]
