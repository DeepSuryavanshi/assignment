from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from rest_framework import generics
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from django.db import IntegrityError 

# CODE TO VENDOR MODELS   
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})


def home(request):
    return render(request,"dashboard.html")


def create_vendor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact_details = request.POST.get('contact_details')
        address = request.POST.get('address')
        vendor_code = request.POST.get('vendor_code')
        # Create and save the new vendor
        Vendor.objects.create(
            name=name,
            contact_details=contact_details,
            address=address,
            vendor_code=vendor_code
        )
        # Display a success message
        messages.success(request, 'Vendor added successfully!')
    return render(request, "create_vendor.html")

def searchvendor(request):
  from django.shortcuts import render
from .models import Vendor


def searchvendor(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        vendors = Vendor.objects.filter(name__icontains=name, address__icontains=address)
    else:
        vendors = Vendor.objects.all()
    return render(request, 'searchvendor.html', {'vendors': vendors})

def delete_vendor(request):
    deletion_message = ""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        try:
            vendor_to_delete = Vendor.objects.get(name=name, address=address)
            vendor_to_delete.delete()
            deletion_message = "Vendor deleted successfully."
        except Vendor.DoesNotExist:
            deletion_message = "Vendor not found."

    vendors = Vendor.objects.all()
    return render(request, "deletevendor.html", {"vendors": vendors, "deletion_message": deletion_message})


def update_vendor(request):
    update_message = ""
    vendor_details = None
    vendors = Vendor.objects.all()

    if request.method == 'POST':
        vendor_code = request.POST.get('vendor_code', '')
        try:
            vendor_details = Vendor.objects.get(vendor_code=vendor_code)
        except Vendor.DoesNotExist:
            update_message = "Vendor with the provided code does not exist."

    return render(request, "update_vendor.html", {"update_message": update_message, "vendor_details": vendor_details, "vendors": vendors})

def save_updated_vendor(request):
    if request.method == 'POST':
        vendor_id = request.POST.get('vendor_id', '')
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        contact_details = request.POST.get('contact_details', '')

        try:
            vendor = Vendor.objects.get(id=vendor_id)
            vendor.name = name
            vendor.address = address
            vendor.contact_details = contact_details
            vendor.save()
            update_message = "Vendor details updated successfully."
        except Vendor.DoesNotExist:
            update_message = "Failed to update vendor details."

        vendors = Vendor.objects.all()
        return render(request, "update_vendor.html", {"update_message": update_message, "vendor_details": None, "vendors": vendors})

#CODE ENDS FOR THE VENDOR

#CODE STARTS FOR PURCHASE ORDER
def purchase_order(request):
    if request.method == 'POST':
        try:
            vendor_id = request.POST.get('vendor')
            vendor = Vendor.objects.get(pk=vendor_id)
            po_number = request.POST.get('po_number')
            order_date = request.POST.get('order_date')
            items = request.POST.get('items')
            quantity = request.POST.get('quantity')
            status = request.POST.get('status')
            
            # Create the PurchaseOrder object
            PurchaseOrder.objects.create(vendor=vendor, po_number=po_number, order_date=order_date, items=items, quantity=quantity, status=status)
            
        except IntegrityError as e:
            print("IntegrityError:", e)  # Print the IntegrityError message for debugging
            error_message = "A Purchase Order with this PO Number already exists. Please choose a unique PO Number."
            vendors = Vendor.objects.all()
            return render(request, 'purchase_order.html', {'error_message': error_message, 'vendors': vendors})

    vendors = Vendor.objects.all() 
    return render(request, 'purchase_order.html', {'vendors': vendors})

def list_purchase_orders(request):
    purchase_orders = PurchaseOrder.objects.all()
    return render(request, 'list_purchases.html', {'purchase_orders': purchase_orders})

# Add other views for viewing, updating, and deleting purchase orders
def view_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
    return render(request, 'view_purchase_order.html', {'purchase_order': purchase_order})

def update_purchase_order(request):
    update_message = ""
    purchase_order_details = None
    purchase_orders = PurchaseOrder.objects.all()

    if request.method == 'POST':
        po_number = request.POST.get('po_number', '')
        try:
            purchase_order_details = PurchaseOrder.objects.get(po_number=po_number)
        except PurchaseOrder.DoesNotExist:
            update_message = "Purchase order with the provided PO number does not exist."

    return render(request, "update_purchase.html", {"update_message": update_message, "purchase_order_details": purchase_order_details, "purchase_orders": purchase_orders})

def save_updated_purchase_order(request):
    if request.method == 'POST':
        purchase_order_id = request.POST.get('purchase_order_id', '')
        items = request.POST.get('items', '')
        quantity = request.POST.get('quantity', '')
        status = request.POST.get('status', '')

        try:
            purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
            purchase_order.items = items
            purchase_order.quantity = quantity
            purchase_order.status = status
            purchase_order.save()
            update_message = "Purchase order details updated successfully."
        except PurchaseOrder.DoesNotExist:
            update_message = "Failed to update purchase order details."

        purchase_orders = PurchaseOrder.objects.all()
        return render(request, "update_purchase.html", {"update_message": update_message, "purchase_order_details": None, "purchase_orders": purchase_orders})
#for delete
def delete_purchase(request):
    deletion_message = ""
    if request.method == 'POST':
        po_number = request.POST.get('po_number', '')
        if po_number:
            try:
                purchase_order_to_delete = PurchaseOrder.objects.get(po_number=po_number)
                purchase_order_to_delete.delete()
                deletion_message = "Purchase order deleted successfully."
            except PurchaseOrder.DoesNotExist:
                deletion_message = "Purchase order not found."

    purchase_orders = PurchaseOrder.objects.all()
    return render(request, "delete_purchase.html", {"purchase_orders": purchase_orders, "deletion_message": deletion_message})
#end for delete 


def search_purchase_orders(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        purchase_orders = PurchaseOrder.objects.filter(
            po_number__icontains=query  # Adjust fields as necessary
        )
    else:
        purchase_orders = PurchaseOrder.objects.all()

    return render(request, 'search_purchase.html', {'purchase_orders': purchase_orders})


#***************************************************************************

class VendorListCreate(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderListCreate(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer



