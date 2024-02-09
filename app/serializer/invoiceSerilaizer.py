from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
from app.models import Invoices

class InvoicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoices
        fields = '__all__'  


    def validate_services_offered(self, value):
        if ',' in value:  # Check if the value contains commas
            services = [service.strip() for service in value.split(',')]

            if any(not service for service in services): # Check if any service is empty or consists only of whitespaces
                raise serializers.ValidationError({'success': False, 'message': 'Each service must not be empty.'})
            return value
        else:
            if not value.strip():# No comma found, treat the whole value as a single service
                raise serializers.ValidationError({'success': False, 'message': 'Service name cannot be empty.'})
            return value
    
    def validate_final_cost(self, value):
        if value <= 0:
            raise serializers.ValidationError({'success': False, 'message': 'Final cost must be a positive number.'})
        return value

    def validate_invoice_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError({'success': False, 'message': 'Invoice date cannot be in the future.'})
        return value
    
    def validate_payment_date(self, value):
        invoice_date_str = self.initial_data.get('invoice_date')
        if not invoice_date_str:
            return value  # If invoice date is not provided, no need for comparison
        invoice_date = datetime.strptime(invoice_date_str, '%Y-%m-%d').date()# Convert invoice_date_str to a datetime.date object

        if value and value < invoice_date:
            raise serializers.ValidationError({'success': False, 'message': 'Payment date cannot be before the invoice date.'})
        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Invoices._meta.get_field('status').choices]
        if value not in valid_statuses:
            raise serializers.ValidationError({'success': False, 'message': 'Invalid invoice status.'})
        return value  

class getInvoicesSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Invoices
        fields = '__all__'
        depth = 1  
