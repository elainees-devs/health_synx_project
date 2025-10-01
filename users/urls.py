# users/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', views.home, name='login'),       # login page
    path('register/', views.register, name='register'),  # register page
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
