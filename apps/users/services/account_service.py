from apps.common.base_service import BaseService
from apps.users.repositories.account_repository import AccountRepository

class AccountService(BaseService):
    def __init__(self):
        super().__init__(AccountRepository())

    def authenticate_user(self, email: str, password: str):
        """Authenticate user with email and password"""
        return self.repository.get_by_credentials(email, password)
    
    def logout_user(self, user=None):
        """Handle user logout - empty function for now"""
        pass