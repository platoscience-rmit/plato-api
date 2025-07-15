from django.utils import timezone
from datetime import timedelta
from apps.assessments.models.assessment_model import Assessment
from apps.assessments.repositories.assessment_repository import AssessmentRepository
from apps.assessments.services.assessment_answer_service import AssessmentAnswerService
from apps.assessments.services.protocol_service import ProtocolService
from apps.common.base_service import BaseService
from django.db import transaction

class AssessmentService(BaseService):
    def __init__(self):
        super().__init__(AssessmentRepository())

    def get_all_by_user(self, user):
        return self.repository.get_all_by_user(user)

    def get_latest_by_user(self, user):
        return self.repository.model.objects.filter(user=user).order_by('-created_at').first()

    def is_valid_time(self, user):
        latest_assessment = self.repository.model.objects.filter(user=user).order_by('-created_at').first()
        if not latest_assessment:
            return True  
        now = timezone.now()
        return (now - latest_assessment.created_at) >= timedelta(seconds=5)

    def create_with_answer_protocol(self, assessment_data, answers_data, suggested_protocol_data):
        try:
            with transaction.atomic():
                assessment = self.create(**assessment_data)

                for answer in answers_data:
                    AssessmentAnswerService().create(assessment=assessment, **answer)
                
                ProtocolService().create_suggested_protocols(assessment=assessment, **suggested_protocol_data)

                return assessment
        except Exception as e:
            raise Exception(f"Error creating assessment: {str(e)}")