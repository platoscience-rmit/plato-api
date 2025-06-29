from apps.common.base_service import BaseService
from apps.users.models.user_model import User
from apps.users.repositories.account_repository import AccountRepository

class AccountService(BaseService):
    def __init__(self):
        super().__init__(AccountRepository())

    def create_account_service(self, email: str, password: str, user_id):
        try:
            user = User.objects.get(id=user_id) 
        except User.DoesNotExist:
            return None
        return self.create(
            email=email,
            password=password,
            user_id=user
        )

   