from rest_framework import serializers
from app.models import Lead_Details
from app.serializer.projectSerializer import ProjectsSerializer

class LeadDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead_Details
        fields = '__all__'  
    
    def validate_email_id(self, value):
        if any(char.isupper() for char in value):
            raise serializers.ValidationError({'success': False, 'message': 'email_id must contain only lowercase letters.'})
        return value