from django.utils import timezone
from datetime import timedelta
from apps.assessments.repositories.assessment_repository import AssessmentRepository
from apps.assessments.services.assessment_answer_service import AssessmentAnswerService
from apps.assessments.services.question_option_service import QuestionOptionService
from apps.assessments.services.question_service import QuestionService
from apps.assessments.services.suggested_protocol_service import SuggestedProtocolService
from apps.notifications.notification_service import NotificationService
from apps.notifications.models.notification_model import Notification
from apps.common.base_service import BaseService
from django.db import transaction
import requests
from apps.common.constants import AI_BASE_URL, MAX_TOKENS

class AssessmentService(BaseService):
    def __init__(self):
        super().__init__(AssessmentRepository())

    def get_all_by_user(self, user):
        assessments = self.repository.get_all_by_user(user)
        selected_protocol = assessments.filter(protocol__isnull=False)
        latest = assessments.order_by('-created_at')[:1]
        return selected_protocol.union(latest).order_by('-created_at')

    def get_latest_by_user(self, user):
        assessment = self.repository.get_latest_by_user(user)
        return assessment

    def end_assessment_period(self):
        four_weeks_ago = timezone.now() - timedelta(weeks=4)
        two_weeks_ago = timezone.now() - timedelta(weeks=2)
        first_result = self.repository.filter(protocol_selected_date__lt=four_weeks_ago,stopped_date__isnull=True)
        second_result = self.repository.filter(
            protocol_selected_date__isnull=True,
            created_at__lt=two_weeks_ago,
            stopped_date__isnull=True
        )
        now = timezone.now()

        first_notifications = [
            Notification(
                user=assessment.user,
                title="Treatment completed",
                description="Conngratulation on your treatment completion! Reassess your condition now and choose a protocol to start another treatment"
            )
            for assessment in first_result
        ]

        second_notifications = [
            Notification(
                user=assessment.user,
                title="Outdated assessment",
                description=f"Your last assessment was created at {assessment.created_at.strftime('%Y-%m-%d %H:%M:%S')} has been considered outdated as you had not started a treatment for more than 14 days. Reassess to refresh your condition and start a new treatment now"
            )
            for assessment in second_result
        ]

        first_count = first_result.update(stopped_date=now)
        second_count = second_result.update(stopped_date=now)
        NotificationService().bulk_create(first_notifications)
        NotificationService().bulk_create(second_notifications)
        
        return first_count + second_count
    
    def end_assessment(self, user, reason):
        latest = self.get_latest_by_user(user)
        if latest:
            latest.stopped_date = timezone.now()
            latest.stop_reason = reason
            latest.save()
            return latest
        return None
        
    def is_stopped(self, user):
        latest_assessment = self.get_latest_by_user(user)
        return latest_assessment.stopped_date is not None
    
    def is_active(self, user):
        latest_assessment = self.get_latest_by_user(user)
        return self.is_stopped(user) is False and latest_assessment.protocol is not None
    
    def can_assess(self, user):
        latest_assessment = self.repository.filter(user=user).order_by('-created_at').first()
        if not latest_assessment:
            return True
        if latest_assessment.protocol is None:
            return True
        return latest_assessment.protocol_selected_date is None or latest_assessment.stopped_date is not None

    def _calculate_scores(self, answers_data):
        phq_questions = QuestionService().group_questions_by_category("phq", answers_data) or []
        bdi_questions = QuestionService().group_questions_by_category("bdi", answers_data) or []
        
        phq_score = QuestionOptionService().sum_of_values(phq_questions) if phq_questions else 0
        bdi_score = QuestionOptionService().sum_of_values(bdi_questions) if bdi_questions else 0
        return phq_score, bdi_score
    
    def _get_plato_score_and_severity(self, phq_score, bdi_score):
        try:
            url = f"{AI_BASE_URL}/assess/"
            payload = {
                "scores": [
                    {"scale": "PHQ-9", "score": phq_score},
                    {"scale": "BDI-II", "score": bdi_score}
                ]
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                raise ValueError(f"Validation Error: {response.text}")

            data = response.json()
            return data.get("plato_score"), data.get("severity_value")
        except Exception as e:
            raise Exception(f"Error retrieving plato_score and severity (PHQ-9: {phq_score}, BDI-II: {bdi_score}): {str(e)}")

        
    def _analyze_depression(self, answers_data):
        try:
            analytic_questions = QuestionService().group_questions_by_category("analytic", answers_data)
            if not analytic_questions:
                return None, None
            query = analytic_questions[0]["answer"]
            
            url = f"{AI_BASE_URL}/analyze-depression/"
            payload = {"query": query, "max_tokens": MAX_TOKENS}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code != 200:
                raise ValueError(f"Validation Error: {response.text}")

            data = response.json()
            return data.get("depression_type"), data.get("analysis"), data.get("short_depression_type")
        except Exception as e:
            raise Exception(f"Error analyzing depression: {str(e)}")
        
    def _get_treatments(self, plato_score):
        try:
            
            url = f"{AI_BASE_URL}/treatment/"
            payload = {"plato_score": plato_score}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code != 200:
                raise ValueError(f"Validation Error: {response.text}")

            data = response.json()
            return data.get("treatments")
        except Exception as e:
            raise Exception(f"Error retrieving suggested protocols: {str(e)}")
    
    def _is_duplicated_question(self, answers_data):
        is_duplicated = True
        questions = []
        for data in answers_data:
            questions.append(data.get('question'))
        if len(questions) == len(set(questions)):
            is_duplicated = False
        return is_duplicated
        
    def create_with_answer(self, assessment_data, user):
        """
        Create a new assessment, save answers, calculate scores,
        and retrieve depression analysis, plato score, severity, and suggested protocols via API AI.

        Args:
            assessment_data (dict): Data containing answers.
            user: The user who is creating the assessment.

        Returns:
            dict: {
                "assessment": Assessment instance,
                "depression_type": str,
                "analysis": str
            }
        """
        answers_data = assessment_data.pop("answers", [])
        if self._is_duplicated_question(answers_data=answers_data):
            raise Exception((f"Error creating assessment: Duplicated question."))
        phq_score, bdi_score = self._calculate_scores(answers_data)
        plato_score, severity = self._get_plato_score_and_severity(phq_score, bdi_score)
        depression_type, analysis, short_depression_type = self._analyze_depression(answers_data)
        treatments = self._get_treatments(plato_score=plato_score)
        study_ids = [t["study_id"] for t in treatments]
        
        try:
            with transaction.atomic():
                record = self.filter(user=user).order_by('-created_at').first()
                if record:
                    record.stopped_date = timezone.now()
                    record.save()
                
                assessment = self.create(
                    **assessment_data, 
                    user=user, 
                    phq_score=phq_score, 
                    bdi_score=bdi_score, 
                    severity=severity,
                    plato_score=plato_score,
                    depression_type=depression_type,
                    analysis=analysis,
                    short_depression_type=short_depression_type
                )
                
                SuggestedProtocolService().create_suggested_protocols(
                    assessment=assessment,
                    treatments=study_ids
                )
                
                for answer in answers_data:
                    QuestionOptionService().validate(answer)
                    AssessmentAnswerService().create(**answer, assessment=assessment)
                
                return {
                    "assessment" : assessment, 
                    "depression_type" : depression_type, 
                    "analysis" : analysis
                }
        except Exception as e:
            raise Exception(f"Error creating assessment: {str(e)}")
        