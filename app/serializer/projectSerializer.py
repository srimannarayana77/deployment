from rest_framework import serializers
from app.models import Projects

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'    
    
    def validate_type(self, value):
        valid_choices = [choice[0] for choice in Projects._meta.get_field('type').choices]
        if value not in valid_choices:
            raise serializers.ValidationError({'success': False, 'message': 'Invalid project type.'})
        return value

    def validate_business_sector(self, value):
        valid_choices = [choice[0] for choice in Projects._meta.get_field('business_sector').choices]
        if value not in valid_choices:
            raise serializers.ValidationError({'success': False, 'message': 'Invalid business sector.'})
        return value    
  
class getProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'business_sector', 'url', 'client', 'created_at', 'updated_at','lead_details']
        depth = 1