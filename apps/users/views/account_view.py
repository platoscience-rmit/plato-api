from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.services.account_service import AccountService
from apps.users.serializers.account_serializer import AccountSerializer
from rest_framework.permissions import IsAuthenticated

class AccountView(APIView):
     
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        
        return [permission() for permission in permission_classes]

    def get(self, request):
        accounts = AccountService().get_all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            try:
                account = AccountService().create(**serializer.validated_data)
                return Response(
                    {
                        'status': 'success',
                        'message': 'Account created successfully',
                        'user': {
                            'email': serializer.validated_data['email'],
                            'user_id': account.id
                        }
                    }, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

class LoginView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            account_service = AccountService()
            account = account_service.authenticate_user(email, password)
            if not account:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            tokens = account_service.generate_tokens(account)
            response = Response({"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                secure=True,
                samesite='Lax',
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            response = Response(
                {
                    'status': 'success',
                    'message': 'Logout successful'
                },
                status=status.HTTP_200_OK
            )
            response.delete_cookie('access_token')
            return response
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
