from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta
import random

class User(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)

    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_code_expires = models.DateTimeField(null=True, blank=True)

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.verification_code_expires = timezone.now() + timedelta(hours=24)
        self.save()
        return self.verification_code
    
    def is_verification_code_valid(self, code):
        return (
            str(self.verification_code) == str(code) and
            self.verification_code_expires and
            timezone.now() < self.verification_code_expires
        )

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