from apps.users.models import Account
from apps.common.base_repository import BaseRepository 

class AccountRepository(BaseRepository):
    def __init__(self):
        super().__init__(Account)

    def create_account_repo(self, email: str, password: str, user_id) -> Account:
        return self.create(
            email=email, 
            password=password, 
            user_id=user_id
        )
