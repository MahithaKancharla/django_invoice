from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from invoiceapp.views import InvoiceViewSet, InvoiceDetailViewSet

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice_details', InvoiceDetailViewSet, basename='invoice_detail')

urlpatterns = [
     path('api/', include(router.urls)),
]

urlpatterns += [
    path('api/invoices/<int:pk>/', InvoiceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='invoic-e'),
    path('api/invoice_details/<int:pk>/', InvoiceDetailViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='invoice-detail'),
]