# from rest_framework import serializers
# from django.contrib.auth.hashers import make_password
# from django.utils import timezone
# from app.models import Client,Projects,Invoices,Lead_Details
    
# class ProjectsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Projects
#         fields = '__all__'    
    
#     def validate_type(self, value):
#         valid_choices = [choice[0] for choice in Projects.TYPE_CHOICES]
#         if value not in valid_choices:
#             raise serializers.ValidationError({'success': False, 'message': 'Invalid project type.'}, status=400)
#         return value

#     def validate_business_sector(self, value):
#         valid_choices = [choice[0] for choice in Projects.BUSINESS_SECTOR_CHOICES]
#         if value not in valid_choices:
#             raise serializers.ValidationError({'success': False, 'message': 'Invalid business sector.'}, status_code=400)
#         return value    


# class InvoicesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoices
#         fields = '__all__'  
    
#     def validate_final_cost(self, value):
#         if value <= 0:
#             raise serializers.ValidationError({'success': False, 'message': 'Final cost must be a positive number.'}, status_code=400)
#         return value

#     def validate_invoice_date(self, value):
#         if value > timezone.now().date():
#             raise serializers.ValidationError({'success': False, 'message': 'Invoice date cannot be in the future.'}, status_code=400)
#         return value

#     def validate_payment_date(self, value):
#         invoice_date = self.initial_data.get('invoice_date')
#         if value and value < invoice_date:
#             raise serializers.ValidationError({'success': False, 'message': 'Payment date cannot be before the invoice date.'}, status_code=400)
#         return value

#     def validate_status(self, value):
#         valid_statuses = [choice[0] for choice in Invoices.STATUS_CHOICES]
#         if value not in valid_statuses:
#             raise serializers.ValidationError({'success': False, 'message': 'Invalid invoice status.'}, status_code=400)
#         return value

#     def validate_project(self, value):
#         if not value.active:
#             raise serializers.ValidationError({'success': False, 'message': 'Associated project is not active.'}, status_code=400)
#         return value


# class ClientSerializer(serializers.ModelSerializer):

#     projects = ProjectsSerializer(many=True, read_only=True)
#     invoices = InvoicesSerializer(many=True, read_only=True)
#     class Meta:
#         model = Client
#         fields = ['id', 'full_name', 'contact_number', 'secondary_number', 'email_address', 'password', 'company_name', 'designation', 'created_at', 'updated_at']
#         extra_kwargs = {'password': {'write_only': True}}
#     def create(self, validated_data):
#         # Hash the password before saving
#         validated_data['password'] = make_password(validated_data.get('password'))
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         # Hash the password before saving
#         if 'password' in validated_data:
#             validated_data['password'] = make_password(validated_data.get('password'))
#         return super().update(instance, validated_data)
    
#     def validate_contact_number(self, value):
#         if len(value) != 10:
#             raise serializers.ValidationError({'success': False, 'message': 'Contact number must be exactly 10 digits.'}, status=400)
#         return value
    
#     def validate_secondary_number(self, value):
#         if  len(value) != 10:
#             raise serializers.ValidationError({'success': False, 'message': 'Secondary number must be exactly 10 digits.'}, status=400)
#         return value
    
#     def validate_email_address(self, value):
#         if any(char.isupper() for char in value):
#             raise serializers.ValidationError({'success': False, 'message': 'email_address must contain only lowercase letters.'}, status=400)
#         return value
    
# class LeadDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lead_Details
#         fields = '__all__'  
    
#     def validate_email_id(self, value):
#         if any(char.isupper() for char in value):
#             raise serializers.ValidationError({'success': False, 'message': 'email_id must contain only lowercase letters.'}, status=400)
#         return value


# class ClientAuthenticationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = ['email_address', 'password']