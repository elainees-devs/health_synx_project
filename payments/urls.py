from django.urls import path
from .views import (
    PaymentListView,
    PaymentDetailView,
    PaymentCreateView,
    PaymentUpdateView,
    PaymentDeleteView,
)

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('create/', PaymentCreateView.as_view(), name='payment-create'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('<int:pk>/update/', PaymentUpdateView.as_view(), name='payment-update'),
    path('<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment-delete'),
]
