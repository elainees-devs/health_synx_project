from django.urls import path
from .views import (
    PrescriptionListView,
    PrescriptionDetailView,
    PrescriptionCreateView,
    PrescriptionUpdateView,
    PrescriptionDeleteView
)

urlpatterns = [
    path('', PrescriptionListView.as_view(), name='prescription-list'),
    path('create/', PrescriptionCreateView.as_view(), name='prescription-create'),
    path('<int:pk>/', PrescriptionDetailView.as_view(), name='prescription-detail'),
    path('<int:pk>/update/', PrescriptionUpdateView.as_view(), name='prescription-update'),
    path('<int:pk>/delete/', PrescriptionDeleteView.as_view(), name='prescription-delete'),
]
