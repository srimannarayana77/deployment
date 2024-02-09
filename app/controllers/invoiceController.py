from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from app.helpers.paginationHelper import paginationResponse
from app.helpers.filters import invoice_filters
from app.helpers.sortHelper import sortHelper
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from app.models import Invoices
from app.serializer.invoiceSerilaizer import InvoicesSerializer,getInvoicesSerializer
from app.constants.messageConstants import *
from rest_framework.exceptions import NotFound
import csv 

class InvoiceView(viewsets.ViewSet):
    @api_view(['POST'])
    def create_invoice(request):
        try:
            serializer = InvoicesSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': CREATE_INVOICE_SUCCESSFULLY, 'data': serializer.data}, status=201)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
    @api_view(['GET']) 
    def retrieve_all_invoices(request):
        try:  
            paginator = PageNumberPagination()

            limit = int(request.query_params.get('limit', 10))
            page = int(request.query_params.get('page', 1))

            paginator.page_size = limit

            sortBy = request.query_params.get('sort_by', 'id')
            sortType = request.query_params.get('sort_type', 'desc')   

            invoices = Invoices.objects.all() 

            invoices = invoice_filters(invoices, request.query_params)

            invoices = sortHelper(sortBy, sortType, invoices)

            page_result = paginator.paginate_queryset(invoices, request)

            serializer = getInvoicesSerializer(page_result, many=True)

            response_data = paginationResponse(ALL_INVOICES_RETRIEVED_SUCCESSFULLY, paginator.page.paginator.count, limit, page, serializer.data)
            return Response(response_data, status=200)  
        except NotFound as e:  # Handle the InvalidPage exception
            return Response({"success": False, "errors": str(e)}, status=400)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
    @api_view(['GET'])  
    def retrieve_single_invoice(request, id):
        try:              
            invoice = Invoices.objects.get(id=id)
            serializer = InvoicesSerializer(invoice)
            return Response({'success': True, 'message': SINGLE_INVOICE_RETRIEVED_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except Invoices.DoesNotExist:
            return Response({'success': False, 'message': INVOICE_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
    
    @api_view(['PUT'])
    def update_invoice(request, id):
        try:
            invoice = Invoices.objects.get(id=id)
            serializer = InvoicesSerializer(invoice, data=request.data)  
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': True, 'message': UPDATE_INVOICE_SUCCESSFULLY, 'data': serializer.data}, status=200)
        except serializers.ValidationError as e:
            return Response({'success': False, 'message': e.detail}, status=422)
        except Invoices.DoesNotExist:
            return Response({'success': False, 'message': INVOICE_NOT_FOUND}, status=404)
        except Exception as err:
            error_message = str(err)
            return Response({'success': False, 'errors': error_message}, status=500)
        
    
    @api_view(['GET'])
    def download_invoice(request, id):
        try:
            invoice = get_object_or_404(Invoices, id=id)# Retrieve the invoice object
            
            serializer = InvoicesSerializer(invoice)# Serialize the invoice data
        
            invoice_data = serializer.data
            
            response = HttpResponse(content_type='csv') # Set the HTTP headers for automatic download

            response['Content-Disposition'] = f'attachment; filename="invoice_{id}.csv"'
            
            csv_writer = csv.writer(response) # Create a CSV writer

            csv_writer.writerow(invoice_data.keys())# Write the CSV header
            
            csv_writer.writerow(invoice_data.values())# Write the invoice data as a row in the CSV file
            
            return response 
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)
        