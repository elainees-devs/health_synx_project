from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_list, name='record-list'),
    path('create/', views.record_create, name='record-create'),
    path('<int:pk>/', views.record_detail, name='record-detail'),
    path('<int:pk>/update/', views.record_update, name='record-update'),
    path('<int:pk>/delete/', views.record_delete, name='record-delete'),
]
