from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        # Create some initial data for testing
        self.invoice = Invoice.objects.create(date='2022-01-01', customer_name='Test Customer')
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Test Item',
            quantity=2,
            unit_price=10.0,
            price=20.0
        )
        Invoice.objects.create(date='2022-01-02', customer_name='Customer 2')
        Invoice.objects.create(date='2022-01-03', customer_name='Customer 3')


    def test_create_invoice(self):
        data = {'date': '2022-02-01', 'customer_name': 'New Customer'}
        response = self.client.post('/api/invoices/', data, format='json')
        print("The newly created invoice using post is: ",response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 4)

    def test_list_invoices(self):
        response = self.client.get('/api/invoices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("List of Invoices:")
        print(response.content.decode('utf-8'))
        self.assertEqual(len(response.data), 3)

    def test_retrieve_invoice(self):
        response = self.client.get(f'/api/invoices/{self.invoice.id}/')
        print("The retrived invoice using get is: ",response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Test Customer')

    def test_update_invoice(self):
        data = {'date': '2022-02-01', 'customer_name': 'Updated Customer'}
        response = self.client.put(f'/api/invoices/{self.invoice.id}/', data, format='json')
        print("The updated invoice using put is: ",response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(Invoice.objects.get(id=self.invoice.id).customer_name, 'Updated Customer')

    def test_partial_update_invoice(self):
        data = {'customer_name': 'Partial Updated Customer'}
        response = self.client.patch(f'/api/invoices/{self.invoice.id}/', data, format='json')
        print("The partially updated invoice using patch is: ",response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get(id=self.invoice.id).customer_name, 'Partial Updated Customer')

    def test_delete_invoice(self):
        response = self.client.delete(f'/api/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 2)

    def test_create_invoice_detail(self):
        data = {'invoice': self.invoice.id, 'description': 'New Item', 'quantity': 3, 'unit_price': 15.0, 'price': 45.0}
        response = self.client.post('/api/invoice_details/', data, format='json')
        print("The newly created invoice_detail using post is: ",response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 2)

    def test_retrieve_invoice_detail(self):
        response = self.client.get(f'/api/invoice_details/{self.invoice_detail.id}/')
        print("The retrived invoice_detail using get is: ",response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Test Item')
    
    def test_update_invoice_detail(self):
        data = {
            'invoice': self.invoice.id,
            'description': 'Updated Item',
            'quantity': 3,
            'unit_price': 15.0,
            'price': 45.0
        }
        response = self.client.put(f'/api/invoice_details/{self.invoice_detail.id}/', data, format='json')
        print("The updated invoice_detail using put is: ",response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(InvoiceDetail.objects.get(id=self.invoice_detail.id).description, 'Updated Item')

    def test_list_invoice_details(self):
        response = self.client.get('/api/invoice_details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("List of Invoices_details:")
        print(response.content.decode('utf-8'))
        self.assertEqual(len(response.data), 1)

    def test_partial_update_invoice_detail(self):
        data = {'description': 'Partial Updated Item'}
        response = self.client.patch(f'/api/invoice_details/{self.invoice_detail.id}/', data, format='json')
        print("The partially updated invoice_detail using patch is: ",response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InvoiceDetail.objects.get(id=self.invoice_detail.id).description, 'Partial Updated Item')

    def test_delete_invoice_detail(self):
        response = self.client.delete(f'/api/invoice_details/{self.invoice_detail.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InvoiceDetail.objects.count(), 0)

    