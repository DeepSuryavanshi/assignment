# Register your models here.
from django.contrib import admin
from .models import Vendor, PurchaseOrder

class display(admin.ModelAdmin):
    list1=('name','contact_information','address')
    list2=('vendor','purchase_order_number','date','total_amount','status')

admin.site.register(Vendor,display)
admin.site.register(PurchaseOrder,display)
