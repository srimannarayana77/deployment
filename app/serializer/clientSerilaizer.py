from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app.models import Client
from app.serializer.projectSerializer import ProjectsSerializer
from app.serializer.invoiceSerilaizer import InvoicesSerializer

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'full_name', 'contact_number', 'secondary_number', 'email_address', 'password', 'company_name', 'designation', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)
    
    def validate_contact_number(self, value):
        value = str(value)  
        if len(value) != 10:
            raise serializers.ValidationError({'success': False, 'message': 'Contact number must be exactly 10 digits.'})
        return value
    
    def validate_secondary_number(self, value):
        if value is not None:
            value = str(value)  
        if  len(value) != 10:
            raise serializers.ValidationError({'success': False, 'message': 'Secondary number must be exactly 10 digits.'})
        return value
    
    def validate_email_address(self, value):
        if any(char.isupper() for char in value):
            raise serializers.ValidationError({'success': False, 'message': 'email_address must contain only lowercase letters.'})
        return value
    
class getClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = ['id', 'full_name', 'contact_number', 'secondary_number', 'email_address', 'company_name', 'designation', 'created_at', 'updated_at','projects','invoices']
        depth = 1
