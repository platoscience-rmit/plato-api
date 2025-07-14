from rest_framework import serializers
from apps.assessments.models import Assessment, Protocol, SuggestedProtocol, AssessmentAnswer
from apps.assessments.models.question_model import Question
from apps.users.models.user_model import User

       
class AnswerSerializer(serializers.ModelSerializer):
    # assessment = serializers.PrimaryKeyRelatedField(queryset=Assessment.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answer = serializers.CharField()
    index = serializers.IntegerField()

    class Meta:
        model = AssessmentAnswer
        fields = [
            'question',
            'answer',
            'index'
        ]


class SuggestedProtocolSerializer(serializers.ModelSerializer):
    # assessment = serializers.PrimaryKeyRelatedField(queryset=Assessment.objects.all())
    first_protocol = serializers.PrimaryKeyRelatedField(queryset=Protocol.objects.all(), allow_null=True, required=False)
    second_protocol = serializers.PrimaryKeyRelatedField(queryset=Protocol.objects.all(), allow_null=True, required=False)
    third_protocol = serializers.PrimaryKeyRelatedField(queryset=Protocol.objects.all(), allow_null=True, required=False)

    class Meta:
        model = SuggestedProtocol
        fields = [
            'first_protocol',
            'second_protocol',
            'third_protocol'
        ]


class AssessmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    phq_score = serializers.IntegerField(min_value=0, max_value=27, allow_null=True)
    bdi_score = serializers.IntegerField(min_value=0, max_value=63, allow_null=True)
    plato_score = serializers.FloatField(min_value=0.0, max_value=27.0, allow_null=True)
    protocol = serializers.PrimaryKeyRelatedField(queryset=Protocol.objects.all(), allow_null=True)
    severity = serializers.IntegerField(min_value=1, max_value=4, allow_null=True)
    answers = AnswerSerializer(many=True, required=False)
    suggested_protocol = SuggestedProtocolSerializer(required=False)

    class Meta:
        model = Assessment
        fields = [
            'user', 
            'phq_score', 
            'bdi_score', 
            'plato_score', 
            'protocol', 
            'severity',
            'answers',
            'suggested_protocol', 
            'created_at'
        ]
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        suggested_data = validated_data.pop("suggested_protocol", None)
        assessment = Assessment.objects.create(**validated_data)
        
        for answer in answers_data:
            AssessmentAnswer.objects.create(assessment=assessment, **answer)

        if suggested_data:
            SuggestedProtocol.objects.create(assessment=assessment, **suggested_data)

        return assessment

class ProtocolSerializer(serializers.ModelSerializer):
    intensity = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    duration = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    node_placement = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    node_type = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    node_size = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)

    class Meta:
        model = Protocol
        fields = [
            'intensity',
            'duration',
            'node_placement',
            'node_type',
            'node_size'
        ]

