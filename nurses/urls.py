# nurses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NursePatientViewSet

router = DefaultRouter()
router.register(r'patients', NursePatientViewSet, basename='nursepatient')

urlpatterns = [
    path('', include(router.urls)),
]
