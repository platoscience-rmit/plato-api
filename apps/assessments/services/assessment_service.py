from apps.assessments.repositories.assessment_repository import AssessmentRepository
from apps.common.base_service import BaseService

class AssessmentService(BaseService):
    def __init__(self):
        super().__init__(AssessmentRepository())

    def get_all_by_user(self, user):
        return self.repository.get_all_by_user(user)
