from django.db import models
from .user_model import User

class Account(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.user_id:
            user = User.objects.create(
                username=self.email,
            )
            self.user = user
        super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        """Always return True for authenticated accounts"""
        return True
    
    @property
    def is_anonymous(self):
        """Always return False for accounts (opposite of is_authenticated)"""
        return False
    
    def __str__(self):
        return self.email