from django.db import models
from .assessment_model import Assessment
from .protocol_model import Protocol

class SuggestedProtocol(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='suggested_protocols')
    first_norm_study = models.CharField(max_length=255, blank=True, null=True)
    second_norm_study = models.CharField(max_length=255, blank=True, null=True)
    third_norm_study = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'assessments_suggested_protocol'

    def get_first_protocol(self):
        return Protocol.objects.filter(norm_study_id=self.first_norm_study).first() if self.first_norm_study else None

    def get_second_protocol(self):
        return Protocol.objects.filter(norm_study_id=self.second_norm_study).first() if self.second_norm_study else None

    def get_third_protocol(self):
        return Protocol.objects.filter(norm_study_id=self.third_norm_study).first() if self.third_norm_study else None

