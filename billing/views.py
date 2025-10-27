# billing/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import BillingRecord
from .serializers import BillingRecordSerializer
from users.permissions import RolePermission
from core.pagination import StandardResultsSetPagination


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="billing.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF <pre>' + html + '</pre>')
    return response


class BillingRecordViewSet(viewsets.ModelViewSet):
    """
    REST API for Billing Records
    """
    queryset = BillingRecord.objects.select_related('patient').order_by('-created_at')
    serializer_class = BillingRecordSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    pagination_class = StandardResultsSetPagination  # add pagination

    @action(detail=False, methods=['get'], url_path='totals')
    def totals(self, request):
        records = self.get_queryset()
        category_totals = (
            records.values('category')
            .annotate(total=Sum('amount'))
            .order_by('category')
        )
        grand_total = records.aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'category_totals': category_totals,
            'grand_total': grand_total,
        })

    @action(detail=True, methods=['post'], url_path='mark-paid')
    def mark_paid(self, request, pk=None):
        record = self.get_object()
        record.paid = True
        record.save()

        category_totals = (
            BillingRecord.objects.filter(patient=record.patient)
            .values('category')
            .annotate(total=Sum('amount'))
        )
        grand_total = (
            BillingRecord.objects.filter(patient=record.patient)
            .aggregate(total=Sum('amount'))['total'] or 0
        )

        context = {
            'record': record,
            'category_totals': category_totals,
            'grand_total': grand_total,
        }

        pdf_response = render_to_pdf('billing/billing_pdf.html', context)
        return pdf_response
