from django.db import models
from apps.users.models import User
from apps.assessments.models.protocol_model import Protocol

class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments')
    madrs_score = models.IntegerField(null=True, blank=True)
    bdi_score = models.IntegerField(null=True, blank=True)
    bmi_score = models.FloatField(null=True, blank=True)
    onDrug = models.BooleanField(default=False)
    chosen_protocol = models.ForeignKey(
        Protocol, 
        on_delete=models.SET_NULL, 
        related_name='assessments', 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
