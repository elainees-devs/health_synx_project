# prescriptions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.prescription_list, name='prescription_list'),                # List all prescriptions
    path('create/', views.prescription_create, name='prescription_create'),     # Create a new prescription
    path('<int:pk>/', views.prescription_detail, name='prescription_detail'),   # View prescription details
    path('<int:pk>/update/', views.prescription_update, name='prescription_update'), # Update prescription
    path('<int:pk>/delete/', views.prescription_delete, name='prescription_delete'), # Delete prescription
]
