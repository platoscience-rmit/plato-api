from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if token is None:
            return None
        validated_token = self.get_validated_token(token)
        print(f"user: {validated_token.payload}")
        user = self.get_user(validated_token)
        return (user, validated_token)