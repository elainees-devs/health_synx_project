# billing/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.billing_list, name='billing_list'),
    path('<int:pk>/', views.billing_detail, name='billing_detail'),
    path('<int:pk>/edit/', views.billing_edit, name='billing_edit'),
    path('<int:pk>/mark-paid/', views.mark_paid, name='billing_mark_paid'),
]
