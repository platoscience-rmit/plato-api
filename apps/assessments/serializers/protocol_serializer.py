from rest_framework import serializers
from apps.assessments.models import Protocol
from apps.assessments.models.norm_study_model import NormStudy

class ProtocolSerializer(serializers.ModelSerializer):
    reference = serializers.SerializerMethodField()
    
    class Meta:
        model = Protocol
        fields = [
            'id',
            'intensity', 
            'duration',
            'node_placement',
            'node_type',
            'node_size',
            'norm_study_id',
            'norm_study_code',
            'tdcs_total_session',
            'tdcs_session_per_week',
            'tdcs_weeks',
            'reference'
        ]
    def get_reference(self, obj):
        norm = NormStudy.objects.filter(id=obj.norm_study_id).first()
        return norm.reference if norm else None