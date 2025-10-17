# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),

     # Dashboards
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('hospital-admin/', views.hospital_admin_dashboard, name='hospital_admin_dashboard'),
    # path('admin/', views.admin_dashboard, name='admin_dashboard'),
]
