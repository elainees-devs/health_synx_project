# doctors/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DoctorViewSet,
    DoctorQueueViewSet,
    DoctorNoteViewSet,
    PrescriptionViewSet,
)

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'queue', DoctorQueueViewSet, basename='doctor-queue')
router.register(r'notes', DoctorNoteViewSet, basename='doctor-note')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [
    path('', include(router.urls)),
]

