# pharmacy/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


# ---------------------------------------------------------------------
# Supplier model: Represents suppliers/vendors of medicines
# ---------------------------------------------------------------------
class Supplier(models.Model):
    """
    Optional: Represents suppliers/vendors of medicines.
    """
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ['id']  # order by supplier id

    
    def __str__(self):
        return self.name

# ---------------------------------------------------------------------
# Medicine model: Represents medicine stocked in the pharmacy
# ---------------------------------------------------------------------
class Medicine(models.Model):
    """
    Represents a medicine stocked in the pharmacy.
    """

    # ---- Medicine Form (Physical Form) ----
    FORM_CHOICES = [
        ('Tablet', 'Tablet'),
        ('Capsule', 'Capsule'),
        ('Syrup', 'Syrup'),
        ('Injection', 'Injection'),
        ('Cream', 'Cream'),
        ('Ointment', 'Ointment'),
        ('Drops', 'Drops'),
        ('Inhaler', 'Inhaler'),
        ('Powder', 'Powder'),
        ('Other', 'Other'),
    ]

    # ---- Medicine Type (Therapeutic Class) ----
    TYPE_CHOICES = [
        ('Antibiotic', 'Antibiotic'),
        ('Analgesic', 'Analgesic'),
        ('Antipyretic', 'Antipyretic'),
        ('Antimalarial', 'Antimalarial'),
        ('Antifungal', 'Antifungal'),
        ('Antiviral', 'Antiviral'),
        ('Antacid', 'Antacid'),
        ('Antidiabetic', 'Antidiabetic'),
        ('Antihypertensive', 'Antihypertensive'),
        ('Vaccine', 'Vaccine'),
        ('Supplement', 'Supplement'),
        ('Cough Syrup', 'Cough Syrup'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name="medicines")

    form = models.CharField(max_length=20, choices=FORM_CHOICES, default='Other', help_text="Physical form of the medicine (Tablet, Capsule, Syrup, etc.)")
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Other', help_text="Therapeutic category (Antibiotic, Painkiller, etc.)")

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id','name']

    def __str__(self):
        return f"{self.name} ({self.form} - {self.type})"

    # Check if medicine has expired
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    
    # Check if the medicine stock is low (threshold <= 10)
    def is_low_stock(self):
        return self.stock <= 10  # configurable threshold
    



# ---------------------------------------------------------------------
# StockTransaction model: Records all stock-related transactions
# ---------------------------------------------------------------------
class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('add', 'Stock Added'),
        ('dispense', 'Medicine Dispensed'),
        ('adjust', 'Stock Adjusted'),
        ('return', 'Medicine Returned'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'pharmacist'}
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        """
        Automatically adjust medicine stock based on transaction type.
        Works for new transactions only.
        """
        is_new = self.pk is None  # True if the transaction is being created for the first time

        if is_new:
            if self.transaction_type == 'add':
                self.medicine.stock += self.quantity
                self.remarks = self.remarks or "Stock automatically increased."
            elif self.transaction_type == 'dispense':
                self.medicine.stock -= self.quantity
                self.remarks = self.remarks or "Stock automatically reduced due to dispensing."
            elif self.transaction_type == 'return':
                self.medicine.stock += self.quantity
                self.remarks = self.remarks or "Returned medicine added back to stock."
            elif self.transaction_type == 'adjust':
                # This allows manual adjustment but records it in remarks
                self.remarks = self.remarks or "Manual stock adjustment recorded."

            # Save updated stock count
            self.medicine.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.medicine.name} ({self.quantity})"