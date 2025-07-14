from apps.assessments.models import Assessment
from apps.common.base_repository import BaseRepository

class AssessmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Assessment)

    def get_all_by_user(self, user):
        return self.filter(user=user).select_related('user').prefetch_related('answers')
