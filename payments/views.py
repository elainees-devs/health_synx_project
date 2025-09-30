from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Payment
from .forms import PaymentForm

# List all payments
class PaymentListView(ListView):
    model = Payment
    template_name = "payments/payment_list.html"
    context_object_name = "payments"
    ordering = ['-created_at']

# View payment details
class PaymentDetailView(DetailView):
    model = Payment
    template_name = "payments/payment_detail.html"
    context_object_name = "payment"

# Create a new payment
class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Add Payment"
        context['submit_button'] = "Create"
        return context

# Update an existing payment
class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Edit Payment"
        context['submit_button'] = "Update"
        return context

# Delete a payment
class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = "payments/payment_confirm_delete.html"
    success_url = reverse_lazy('payment-list')
