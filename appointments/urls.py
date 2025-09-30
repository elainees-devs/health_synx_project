# appointments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),# List all appointments
    path('create/', views.appointment_create, name='appointment_create'),  # Create a new appointment
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),# View appointment details
    path('<int:pk>/update/', views.appointment_update, name='appointment_update'), # Update appointment
    path('<int:pk>/delete/', views.appointment_delete, name='appointment_delete'), # Delete appointment
]
