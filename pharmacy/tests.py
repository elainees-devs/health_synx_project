# pharmacy/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import Supplier, Medicine, StockTransaction

User = get_user_model()


class SupplierModelTest(TestCase):
    def test_create_supplier(self):
        supplier = Supplier.objects.create(
            name="MedPlus Distributors",
            contact_person="Jane Doe",
            phone="0712345678",
            email="info@medplus.com",
            address="Nairobi, Kenya"
        )

        self.assertEqual(str(supplier), "MedPlus Distributors")
        self.assertEqual(supplier.phone, "0712345678")
        self.assertTrue(Supplier.objects.exists())


class MedicineModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(name="Health Suppliers Ltd")
        self.medicine = Medicine.objects.create(
            name="Paracetamol",
            description="Pain relief and fever reducer",
            supplier=self.supplier,
            form="Tablet",
            type="Antipyretic",
            price=120.00,
            stock=8,
            expiry_date=timezone.now().date() + timedelta(days=10)
        )

    def test_string_representation(self):
        expected = "Paracetamol (Tablet - Antipyretic)"
        self.assertEqual(str(self.medicine), expected)

    def test_is_low_stock(self):
        self.assertTrue(self.medicine.is_low_stock())

        self.medicine.stock = 15
        self.medicine.save()
        self.assertFalse(self.medicine.is_low_stock())

    def test_is_expired(self):
        self.medicine.expiry_date = timezone.now().date() - timedelta(days=1)
        self.assertTrue(self.medicine.is_expired())

        self.medicine.expiry_date = timezone.now().date() + timedelta(days=5)
        self.assertFalse(self.medicine.is_expired())


class StockTransactionModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(name="Pharma Suppliers")
        self.medicine = Medicine.objects.create(
            name="Amoxicillin",
            price=250.00,
            stock=50,
            supplier=self.supplier
        )
        self.pharmacist = User.objects.create_user(
            username="pharmacist1",
            password="strongpassword",
        )

    def test_add_stock_transaction_increases_stock(self):
        StockTransaction.objects.create(
            medicine=self.medicine,
            transaction_type="add",
            quantity=10,
            performed_by=self.pharmacist
        )
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, 60)

    def test_dispense_transaction_decreases_stock(self):
        StockTransaction.objects.create(
            medicine=self.medicine,
            transaction_type="dispense",
            quantity=5,
            performed_by=self.pharmacist
        )
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, 45)

    def test_return_transaction_increases_stock(self):
        StockTransaction.objects.create(
            medicine=self.medicine,
            transaction_type="return",
            quantity=5,
            performed_by=self.pharmacist
        )
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, 55)

    def test_adjust_transaction_does_not_change_stock(self):
        initial_stock = self.medicine.stock
        StockTransaction.objects.create(
            medicine=self.medicine,
            transaction_type="adjust",
            quantity=3,
            performed_by=self.pharmacist
        )
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.stock, initial_stock)
