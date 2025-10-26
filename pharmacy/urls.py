# pharmacy/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineViewSet, SupplierViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [
    # REST API
    path('api/', include(router.urls)),
]

