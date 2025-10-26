# diagnostics/utils.py
from billing.models import BillingRecord
from datetime import datetime

# Fixed fees
DIAGNOSTIC_FEES = {
    'lab': 500,
    'xray': 3000,
    'mri': 4000,
}

def create_diagnostic_fee(patient, queue_item, test_type):
    """
    Create a billing record for a completed diagnostic test.
    
    Parameters:
    - patient: User instance
    - queue_item: LabQueue, XRayQueue, or MRIQueue instance
    - test_type: 'lab', 'xray', or 'mri'
    """

    if test_type not in DIAGNOSTIC_FEES:
        raise ValueError("Invalid diagnostic test type")

    amount = DIAGNOSTIC_FEES[test_type]
    description = f"{test_type.upper()} Test Fee"

    # Create a billing record
    billing_record = BillingRecord.objects.create(
        patient=patient,
        amount=amount,
        description=description,
        paid=False,
        created_at=datetime.now()
    )

    return billing_record
