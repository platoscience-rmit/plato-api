from apps.common.base_service import BaseService
from apps.users.models.user_model import User
from apps.users.repositories.account_repository import AccountRepository

class AccountService(BaseService):
    def __init__(self):
        super().__init__(AccountRepository())
