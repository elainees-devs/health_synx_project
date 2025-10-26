# billing/utils.py
from .models import BillingRecord

def create_consultation_fee(patient, doctor_queue, amount=1200.00):
    """
    Create a BillingRecord for the doctor's consultation fee.
    """
    BillingRecord.objects.create(
        patient=patient,
        doctor_queue=doctor_queue,
        category='consultation',
        description='Doctor Consultation Fee',
        amount=amount
    )


def create_pharmacy_fee(patient, doctor_queue, amount):
    """
    Create a BillingRecord for pharmacy charges.
    """
    BillingRecord.objects.create(
        patient=patient,
        doctor_queue=doctor_queue,
        category='pharmacy',
        description='Pharmacy Dispensing & Medicine Charges',
        amount=amount
    )
