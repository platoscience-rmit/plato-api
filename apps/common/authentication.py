from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from apps.users.models import Account
class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if token is None:
            return None
        
        try:
            validated_token = self.get_validated_token(token)
            
            account_id = validated_token.payload.get('account_id')
            if not account_id:
                user_id = validated_token.payload.get('user_id')
                if user_id:
                    try:
                        account = Account.objects.select_related('user').get(user_id=user_id)
                        return (account, validated_token)
                    except Account.DoesNotExist:
                        return None
                return None
            
            try:
                account = Account.objects.select_related('user').get(id=account_id)
                return (account, validated_token)
            except Account.DoesNotExist:
                return None
                
        except TokenError:
            return None