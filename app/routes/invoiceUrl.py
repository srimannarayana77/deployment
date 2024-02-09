from django.urls import path
from app.controllers.invoiceController import InvoiceView

urlpatterns = [
    path('', InvoiceView.create_invoice),
    path('<int:id>', InvoiceView.retrieve_single_invoice),
    path('<int:id>/update',InvoiceView.update_invoice),
    # path('<int:id>/delete',InvoiceView.delete_invoice),
    path('all', InvoiceView.retrieve_all_invoices),
    path('<int:id>/download',InvoiceView.download_invoice)
]