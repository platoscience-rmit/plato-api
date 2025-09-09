from django.db import models

class Protocol(models.Model):
    intensity = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    node_placement = models.CharField(max_length=255, blank=True, null=True)
    node_type = models.CharField(max_length=255, blank=True, null=True)
    node_size = models.CharField(max_length=255, blank=True, null=True)
    norm_study_id = models.CharField(max_length=255, blank=True, null=True)
    norm_study_code = models.CharField(max_length=255, blank=True, null=True)
    tdcs_total_session = models.CharField(max_length=255, blank=True, null=True)
    tdcs_session_per_week = models.CharField(max_length=255, blank=True, null=True)
    tdcs_weeks = models.CharField(max_length=255, blank=True, null=True)