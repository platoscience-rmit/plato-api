from apps.users.models import Account
from apps.common.base_repository import BaseRepository 

class AccountRepository(BaseRepository):
    def __init__(self):
        super().__init__(Account)

