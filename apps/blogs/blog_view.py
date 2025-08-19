from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.blogs.blog_service import BlogService
from apps.blogs.blog_serializer import BlogSerializer

class BlogView(APIView):
    
    def __init__(self):
        self.service = BlogService()
        
    def get(self, request):
        try:
            data = self.service.get_all()
            return Response(BlogSerializer(data, many=True).data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
            