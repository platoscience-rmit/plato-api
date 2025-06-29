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


class CreateAccountView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            return Response(
                {
                    'status': 'success',
                    'message': 'Account created successfully',
                    'user': {
                        'email': account.email,
                        'user_id': account.id
                    }
                }, 
                status=status.HTTP_201_CREATED
            )
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


