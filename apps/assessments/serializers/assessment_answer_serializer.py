from rest_framework import serializers
from apps.assessments.models import AssessmentAnswer, Question
from apps.assessments.serializers.question_serializer import QuestionSerializer
from apps.assessments.serializers.question_option_serializer import QuestionOptionSerializer
class AssessmentAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    assessment = serializers.PrimaryKeyRelatedField(read_only=True)
    selected_option = QuestionOptionSerializer(read_only=True)

    class Meta:
        model = AssessmentAnswer
        fields = [
            'id',
            'assessment',
            'question',
            'answer',
            'selected_option',
            'index',
        ]