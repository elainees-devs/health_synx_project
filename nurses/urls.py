# nurses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.nurse_dashboard, name='nurse_dashboard'),              
    path('patients/', views.patient_list, name='patient_list'),  
]
