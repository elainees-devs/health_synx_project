from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('patients.urls')),
    path('patient/', include('patients.urls')),
    path('doctor/', include('doctors.urls')),
    path('appointment/', include('appointments.urls')),
]
