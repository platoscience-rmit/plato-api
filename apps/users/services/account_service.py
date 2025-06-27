from apps.common.base_service import BaseService
from apps.users.repositories.account_repository import AccountRepository

class AccountService(BaseService):
    def __init__(self):
        super().__init__(AccountRepository())
        self.account_repo = AccountRepository()

    def create_account_service(self, email: str, password: str, user_id):
        return self.account_repo.create_account_repo(
            email=email,
            password=password,
            user_id=user_id
        )

   