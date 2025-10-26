# billing/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillingRecordViewSet

# Create a DRF router and register the BillingRecordViewSet
router = DefaultRouter()
router.register(r'billing', BillingRecordViewSet, basename='billing')

urlpatterns = [
    path('', include(router.urls)),
]
