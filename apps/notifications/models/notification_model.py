from django.db import models
from apps.users.models.user_model import User

class Notification(models.Model):
    class Type(models.TextChoices):
        OUTDATED = "OUTDATED", "Outdated assessment"
        COMPLETE = "COMPLETE", "Treatment completed"

    type = models.CharField(
        max_length=50, 
        choices=Type.choices,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=50)
    description = models.CharField()
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        related_name='notifications', 
        null=True, 
        blank=True
    )
    is_readed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    assessment_time = models.DateTimeField(null=True, blank=True)