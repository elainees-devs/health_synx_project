# billing/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from xhtml2pdf import pisa

from users.decorators import role_required
from .models import BillingRecord
from .forms import BillingRecordForm

def render_to_pdf(template_src, context_dict={}):
    """Render a Django template to PDF using xhtml2pdf"""
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="billing.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF <pre>' + html + '</pre>')
    return response

@role_required(allowed_roles=['admin', 'billing'])
def billing_list(request):
    """View all billing records"""
    records = BillingRecord.objects.all().order_by('-created_at')
    return render(request, 'billing/billing_list.html', {'records': records})

@role_required(allowed_roles=['admin', 'billing'])
def billing_detail(request, pk):
    """View a single billing record"""
    record = get_object_or_404(BillingRecord, pk=pk)
    return render(request, 'billing/billing_detail.html', {'record': record})

@role_required(allowed_roles=['admin', 'billing'])
def billing_edit(request, pk):
    """Edit an existing billing record"""
    record = get_object_or_404(BillingRecord, pk=pk)
    if request.method == 'POST':
        form = BillingRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('billing_list')
    else:
        form = BillingRecordForm(instance=record)

    return render(request, 'billing/billing_edit.html', {'form': form, 'record': record})

@role_required(allowed_roles=['admin', 'billing'])
def mark_paid(request, pk):
    """Mark billing record as paid and generate PDF"""
    record = get_object_or_404(BillingRecord, pk=pk)
    record.paid = True
    record.save()
    context = {'record': record}
    return render_to_pdf('billing/billing_pdf.html', context)


@role_required(allowed_roles=['admin', 'billing'])
def no_permission(request):
    """Page shown when user does not have access"""
    return render(request, 'billing/no_permission.html')

