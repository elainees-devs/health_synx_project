# health_synx/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from users import views as user_views

def redirect_root(request):
    return redirect('login') #'redirect_after_login'

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', redirect_root),  # handles the root URL
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', user_views.register_user, name='register'), 
    path('redirect-after-login/', user_views.redirect_after_login, name='redirect_after_login'),  
    path('departments/', include('departments.urls')),
    path('users/', include('users.urls')),
    path('nurses/', include('nurses.urls')),
    path('doctors/', include('doctors.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('billing/', include('billing.urls')),
]
