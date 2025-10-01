from django.contrib import admin
from django.urls import path, include

from users.views import home 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('user/', include('users.urls')),
    path('patient/', include('patients.urls')),
    path('doctor/', include('doctors.urls')),
    path('appointment/', include('appointments.urls')),
    path('prescription/', include('prescriptions.urls')),
    path('payment/', include('payments.urls')),
]
