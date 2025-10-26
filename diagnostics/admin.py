# diagnostics/admin.py
from django.contrib import admin
from .models import (
    LabTest, LabQueue,
    XRay, XRayQueue,
    MRI, MRIQueue
)


# -----------------------------
# LAB ADMIN
# -----------------------------
@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'normal_range', 'created_at')
    search_fields = ('name', 'normal_range')
    list_filter = ('created_at',)
    ordering = ('name',)


@admin.register(LabQueue)
class LabQueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'lab_test', 'technician', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__username', 'lab_test__name')
    autocomplete_fields = ('patient', 'lab_test', 'technician')
    ordering = ('-created_at',)


# -----------------------------
# XRAY ADMIN
# -----------------------------
@admin.register(XRay)
class XRayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)


@admin.register(XRayQueue)
class XRayQueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'xray', 'technician', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__username', 'xray__name')
    autocomplete_fields = ('patient', 'xray', 'technician')
    ordering = ('-created_at',)


# -----------------------------
# MRI ADMIN
# -----------------------------
@admin.register(MRI)
class MRIAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)


@admin.register(MRIQueue)
class MRIQueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'mri', 'technician', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__username', 'mri__name')
    autocomplete_fields = ('patient', 'mri', 'technician')
    ordering = ('-created_at',)
