from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.services.account_service import AccountService
from apps.users.serializers.account_serializer import AccountSerializer

class AccountListView(APIView):
    def get(self, request):
        accounts = AccountService().get_all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user_id = request.data.get('user_id')

        if not email or not password or not user_id:
            return Response(
                {'error': 'Email, password and user_id are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        account = AccountService().create_account_service(
            email=email,
            password=password,
            user_id=user_id
        )

        if account:
            return Response(
                {
                    'status': 'success',
                    'message': 'Account created successfully',
                    'user': {
                        'id': account.user_id.id,
                        'username': account.user_id.username,
                        'email': account.email,
                        'is_verified': account.is_verified
                    }
                }, 
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': 'error',
                    'message': 'Account creation failed'
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


