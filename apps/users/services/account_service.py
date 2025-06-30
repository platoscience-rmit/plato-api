from apps.common.base_service import BaseService
from apps.users.models.user_model import User
from apps.users.repositories.account_repository import AccountRepository
from rest_framework_simplejwt.tokens import RefreshToken

class AccountService(BaseService):
    def __init__(self):
        super().__init__(AccountRepository())

    def authenticate_user(self, email: str, password: str):
        account = self.repository.get_by_credentials(email, password)
        if not account:
            return None
        return account

    def generate_tokens(self, account):
        if not account.user:
            raise ValueError("Account must have an associated user to generate tokens")
        
        refresh = RefreshToken.for_user(account.user)
        refresh['account_id'] = account.id
        refresh['email'] = account.email
        refresh['is_verified'] = account.is_verified
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


