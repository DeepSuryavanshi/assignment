import datetime
from datetime import timedelta
from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import timedelta
from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100, default="Default Name")
    contact_details = models.CharField(max_length=200, default="No contact details provided")
    address = models.TextField(default="No address provided")
    vendor_code = models.CharField(max_length=50, unique=True, default='DEFAULT')
    

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateField(default=datetime.now)  # Default value set to current date and time
    items = models.TextField(default='No items')  # Default value set to 'No items'
    quantity = models.PositiveIntegerField(default=0)  # Default value set to 0
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor.name}"
    

    class VendorPerformance(models.Model):
        vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
        on_time_delivery_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
        quality_rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
        response_time = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
        fulfilment_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])


