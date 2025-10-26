# patients/admin.py
from django.contrib import admin
from .models import (
    PatientProfile,
    PatientVitals,
    DoctorQueue,
    DoctorNote,
    Prescription,
    PrescriptionItem,
)


# ----------------------------
# Patient Profile
# ----------------------------
@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "get_full_name", "get_email", "assigned_doctor", "dob")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    list_filter = ("assigned_doctor",)
    autocomplete_fields = ("user", "assigned_doctor")

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = "Full Name"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"


# ----------------------------
# Patient Vitals
# ----------------------------
@admin.register(PatientVitals)
class PatientVitalsAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "temperature", "pulse_rate", "recorded_at")
    search_fields = ("patient__username", "patient__email", "patient__first_name", "patient__last_name")
    list_filter = ("recorded_at",)
    autocomplete_fields = ("patient",)
    ordering = ("-recorded_at",)


# ----------------------------
# Doctor Queue
# ----------------------------
@admin.register(DoctorQueue)
class DoctorQueueAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at", "doctor")
    search_fields = ("patient__username", "doctor__username")
    autocomplete_fields = ("patient", "doctor", "vitals")
    ordering = ("-created_at",)


# ----------------------------
# Doctor Notes
# ----------------------------
@admin.register(DoctorNote)
class DoctorNoteAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "queue_item", "created_at")
    search_fields = ("patient__username", "doctor__username", "diagnosis")
    list_filter = ("created_at",)
    autocomplete_fields = ("patient", "doctor", "queue_item")
    ordering = ("-created_at",)


# ----------------------------
# Prescription
# ----------------------------
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "status", "date_issued")
    search_fields = ("patient__username", "doctor__username")
    list_filter = ("status", "date_issued")
    autocomplete_fields = ("patient", "doctor", "queue_item")
    ordering = ("-date_issued",)


# ----------------------------
# Prescription Items
# ----------------------------
@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "prescription", "medicine", "dosage")
    search_fields = ("medicine__name", "prescription__patient__username")
    autocomplete_fields = ("prescription", "medicine")
