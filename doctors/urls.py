# doctors/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('queue/', views.doctor_queue, name='doctor_queue'),
    path('queue/update/<int:queue_id>/<str:action>/', views.update_queue_status, name='update_queue_status'),
    path('queue/<int:queue_id>/see/', views.see_patient, name='see_patient'),
]
