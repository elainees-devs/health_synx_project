# hospital_admins/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HospitalAdminViewSet, register_hospital_admin

router = DefaultRouter()
router.register(r'', HospitalAdminViewSet, basename='hospital-admins')

urlpatterns = [
    # DRF endpoints (list, create, retrieve, update, delete)
    path('api/', include(router.urls)),

    # Optional traditional form registration (if still used in templates)
    path('register/', register_hospital_admin, name='register_hospital_admin'),
]
