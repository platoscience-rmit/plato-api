from django.db import models
from .user_model import User

class Account(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')