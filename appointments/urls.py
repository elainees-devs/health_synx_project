# appointments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Patient URLs
    path('book/', views.book_appointment, name='book_appointment'),
    path('patient-appointments/', views.patient_appointments, name='patient_appointments'),  
    path('doctor/', views.doctor_appointments, name='doctor_appointments'),
    path('all/', views.all_appointments, name='all_appointments'),
]
