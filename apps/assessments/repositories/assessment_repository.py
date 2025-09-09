from apps.assessments.models import Assessment
from apps.common.base_repository import BaseRepository
from django.db.models import Count

class AssessmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Assessment)

    def get_all_by_user(self, user):
        return (self.filter(user=user)
                .select_related('user', 'protocol')
                .prefetch_related(
                    'answers', 
                    'answers__selected_option', 
                    'suggested_protocols')
                ).annotate(checkin_days_count=Count("checkin_answers__checkin_date", distinct=True))
    
    def get_latest_by_user(self, user):
        return (self.filter(user=user)
                    .select_related('protocol')
                    .prefetch_related('suggested_protocols', 'answers')
                    .annotate(checkin_days_count=Count("checkin_answers__checkin_date", distinct=True))
                    .order_by('-created_at')
                    .first())
