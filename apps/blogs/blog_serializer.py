from rest_framework import serializers
from apps.blogs.models.blog_model import Blog

class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog    
        fields = '__all__'