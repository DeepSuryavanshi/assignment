from django.urls import path
from .views import VendorListCreate,VendorRetrieveUpdateDestroy
from django.urls import path
from . import views

urlpatterns = [
   path('vendors/', views.VendorListCreate.as_view(), name='vendor-list-create'),
   path('vendors/<int:pk>/', views.VendorRetrieveUpdateDestroy.as_view(), name='vendor-retrieve-update-destroy'),
   path('purchase_orders/', views.PurchaseOrderListCreate.as_view(), name='purchaseorder-list-create'),
   path('purchase_orders/<int:pk>/', views.PurchaseOrderRetrieveUpdateDestroy.as_view(), name='purchaseorder-retrieve-update-destroy'),
   path('vendor_list/', views.vendor_list, name='vendor-list')
]
