# health_synx/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect

from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users import views as user_views


# Redirect root to Swagger UI
def redirect_root(request):
    return redirect('schema-swagger-ui')


# Swagger/OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="HealthSynx API",
        default_version='v1',
        description="API documentation for HealthSynx project",
        contact=openapi.Contact(email="support@healthsynx.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', redirect_root),

    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API-based authentication
    path('api/login/', user_views.LoginAPIView.as_view(), name='api_login'),
    path('register/', user_views.register_user, name='register'),
    path('redirect-after-login/', user_views.redirect_after_login, name='redirect_after_login'),

    # App routes
    path('departments/', include('departments.urls')),
    path('users/', include('users.urls')),
    path('nurses/', include('nurses.urls')),
    path('doctors/', include('doctors.urls')),
    path('diagnostics/', include('diagnostics.urls')),
    path('patients/', include('patients.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('appointments/', include('appointments.urls')),
    path('billing/', include('billing.urls')),

    # Swagger/OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
