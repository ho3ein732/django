# urls.py

from django.urls import path
from api.views import InvoiceDetailApiView, AddToInvoiceApiView, UpdateInvoiceItemApiView, RemoveInvoiceItemApiView
app_name = "invoice"


urlpatterns = [
    path('invoice/', InvoiceDetailApiView.as_view(), name='invoice-detail'),
    path('invoice/add/', AddToInvoiceApiView.as_view(), name='invoice-add'),
    path('invoice/update/<pk>', UpdateInvoiceItemApiView.as_view(), name='invoice-update'),
    path('invoice/remove/<pk>', RemoveInvoiceItemApiView.as_view(), name='invoice-remove'),
]

