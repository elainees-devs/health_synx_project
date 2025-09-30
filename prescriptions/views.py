from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Prescription
from .forms import PrescriptionForm

# List all prescriptions
class PrescriptionListView(ListView):
    model = Prescription
    template_name = "prescriptions/prescription_list.html"
    context_object_name = "prescriptions"
    ordering = ['id']

# View prescription details
class PrescriptionDetailView(DetailView):
    model = Prescription
    template_name = "prescriptions/prescription_detail.html"
    context_object_name = "prescription"

# Create a new prescription
class PrescriptionCreateView(CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "prescriptions/prescription_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Add Prescription"
        context['submit_button'] = "Create"
        return context

# Update an existing prescription
class PrescriptionUpdateView(UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "prescriptions/prescription_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Edit Prescription"
        context['submit_button'] = "Update"
        return context

# Delete a prescription
class PrescriptionDeleteView(DeleteView):
    model = Prescription
    template_name = "prescriptions/prescription_confirm_delete.html"
    success_url = reverse_lazy('prescription-list')
