# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  
from .views import register_patient, UserListView

# DRF router (for future API endpoints like /api/users/)
router = DefaultRouter()
# Example: router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # Authentication routes (no templates)
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path('register/patient/', register_patient, name='register_patient'),

    # REST-style dashboard endpoints
    path('doctor/', views.DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('hospital-admin/', views.HospitalAdminDashboardView.as_view(), name='hospital_admin_dashboard'),
    path('nurse/', views.NurseDashboardView.as_view(), name='nurse_dashboard'),
    path('pharmacy/', views.PharmacyDashboardView.as_view(), name='pharmacy_dashboard'),
    path('billing/', views.BillingDashboardView.as_view(), name='billing_dashboard'),

  # Admin-only: get all users
    path('users/', UserListView.as_view(), name='user-list'),


    # Optional: include DRF router endpoints
    path('api/', include(router.urls)),
]
