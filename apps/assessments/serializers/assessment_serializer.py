from rest_framework import serializers
from apps.assessments.models import Assessment
from apps.assessments.serializers.assessment_answer_serializer import AssessmentAnswerSerializer

class AssessmentSerializer(serializers.ModelSerializer):
    answers = AssessmentAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = [
            'id',
            'user',
            'phq_score',
            'bdi_score',
            'plato_score',
            'protocol',
            'severity',
            'answers',
            'created_at',
        ]
