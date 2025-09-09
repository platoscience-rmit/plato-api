from django.db import models

class NormStudy(models.Model):
    study_code = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'treatment_system"."norm_study'
        managed = False
