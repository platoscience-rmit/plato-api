from apps.common.base_service import BaseService
from apps.users.models.user_model import User
from apps.users.repositories.account_repository import AccountRepository
from rest_framework_simplejwt.tokens import RefreshToken

class AccountService(BaseService):
    def __init__(self):
        super().__init__(AccountRepository())

    def authenticate_user(self, email: str, password: str):
        """Authenticate user with email and password"""
        account = self.repository.get_by_credentials(email, password)
        if not account:
            return None
        return account

    def generate_tokens(self, user):
        """Generate JWT tokens for the authenticated user"""
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def logout_user(self, user=None):
        """Handle user logout by blacklisting the refresh token"""
        if user:
            refresh_token = RefreshToken.for_user(user)
            refresh_token.blacklist()
