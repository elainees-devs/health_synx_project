# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('logout/', views.logout_view, name='logout'), 
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),

    # Dashboards
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('hospital-admin/', views.hospital_admin_dashboard, name='hospital_admin_dashboard'),
    path('nurse/', views.nurse_dashboard, name='nurse_dashboard'),
    path('billing/', views.billing_dashboard, name='billing_dashboard'),
]
