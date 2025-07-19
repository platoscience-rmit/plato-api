from apps.assessments.repositories.question_repository import QuestionRepository
from apps.common.base_service import BaseService

class QuestionService(BaseService):
    def __init__(self):
        super().__init__(QuestionRepository())
