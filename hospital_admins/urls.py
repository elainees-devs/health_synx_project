# hospital_admins/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_hospital_admin, name='register_hospital_admin'),
    # path('list/', views.hospital_admin_list, name='hospital_admin_list'),
    # path('edit/<int:pk>/', views.edit_hospital_admin, name='edit_hospital_admin'),
    # path('delete/<int:pk>/', views.delete_hospital_admin, name='delete_hospital_admin'),
]
