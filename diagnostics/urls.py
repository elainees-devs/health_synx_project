# diagnostics/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LabTestViewSet,
    LabQueueViewSet,
    XRayViewSet,
    XRayQueueViewSet,
    MRIViewSet,
    MRIQueueViewSet,
)

router = DefaultRouter()

# -----------------------------
# LAB ROUTES
# -----------------------------
router.register(r'lab/tests', LabTestViewSet, basename='lab-test')
router.register(r'lab/queue', LabQueueViewSet, basename='lab-queue')

# -----------------------------
# XRAY ROUTES
# -----------------------------
router.register(r'xray/tests', XRayViewSet, basename='xray-test')
router.register(r'xray/queue', XRayQueueViewSet, basename='xray-queue')

# -----------------------------
# MRI ROUTES
# -----------------------------
router.register(r'mri/tests', MRIViewSet, basename='mri-test')
router.register(r'mri/queue', MRIQueueViewSet, basename='mri-queue')

urlpatterns = [
    path('', include(router.urls)),
]
