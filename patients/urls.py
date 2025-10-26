# patients/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')

urlpatterns = [
    # Include DRF router URLs
    path('api/', include(router.urls)),
]
