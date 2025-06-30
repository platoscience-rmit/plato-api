from apps.users.models import Account
from apps.common.base_repository import BaseRepository 

class AccountRepository(BaseRepository):
    def __init__(self):
        super().__init__(Account)
    
    def get_by_credentials(self, email: str, password: str):
        """Get account by email and password for authentication"""
        accounts = self.filter(email=email, password=password)
        
        return accounts.select_related('user').first()
