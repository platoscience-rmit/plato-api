from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    
    @property
    def is_authenticated(self):
        """Always return True for authenticated users"""
        return True
    
    @property
    def is_anonymous(self):
        """Always return False for users (opposite of is_authenticated)"""
        return False
    
    def __str__(self):
        return self.email