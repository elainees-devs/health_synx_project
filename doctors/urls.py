# doctors/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),    # List all doctors
    path('create/', views.doctor_create, name='doctor_create'),# Create a new doctor
    path('<int:pk>/', views.doctor_detail, name='doctor_detail'),    # View doctor details
    path('<int:pk>/update/', views.doctor_update, name='doctor_update'), # Update doctor
    path('<int:pk>/delete/', views.doctor_delete, name='doctor_delete'), # Delete doctor
]
