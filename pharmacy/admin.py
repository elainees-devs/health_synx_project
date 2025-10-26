# pharmacy/admin.py
from django.contrib import admin
from .models import Medicine, StockTransaction, Supplier

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'price', 'expiry_date', 'is_expired', 'is_low_stock')
    search_fields = ('name',)
    list_filter = ('expiry_date',)

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'transaction_type', 'quantity', 'performed_by', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('medicine__name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name',)
