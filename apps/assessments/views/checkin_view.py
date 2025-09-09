from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.assessments.models import Assessment
from apps.assessments.services.assessment_service import AssessmentService
from apps.assessments.services.assessment_checkin_answer_service import AssessmentCheckinAnswerService
from apps.assessments.serializers.assessment_checkin_answer_serializer import CheckInHistoryDaySerializer, AssessmentCheckinAnswerSerializer
from django.db.models.functions import TruncDate
from apps.assessments.schemas.check_in_schema import checkin_history_schema, checkin_questions_schema, checkin_submit_schema
from apps.assessments.services.question_service import QuestionService
from apps.assessments.serializers.question_serializer import QuestionSerializer
from apps.assessments.services.question_option_service import QuestionOptionService
from django.utils import timezone
from apps.assessments.serializers.assessment_serializer import AssessmentSerializer
from django.db import transaction

class CheckinValidationError(Exception):
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
        
class CheckInHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.assessment_service = AssessmentService()
        self.assessment_checkin_answer_service = AssessmentCheckinAnswerService()

    @checkin_history_schema
    def get(self, request, assessment_id):
        assessment = self.assessment_service.get_by_id(assessment_id)
        if not assessment or assessment.user != request.user:
            return Response({'error': 'Assessment not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

        history = self.assessment_checkin_answer_service.get_checkin_history(assessment)
        serializer = CheckInHistoryDaySerializer(history, many=True)
        return Response({'checkin_history': serializer.data}, status=status.HTTP_200_OK)
    
class CheckInQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.question_service = QuestionService()

    @checkin_questions_schema
    def get(self, request):
        try:
            questions = self.question_service.filter(category='check-in')
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.assessment_service = AssessmentService()
        self.assessment_checkin_answer_service = AssessmentCheckinAnswerService()
        self.question_service = QuestionService()
        self.question_option_service = QuestionOptionService()

    @checkin_submit_schema
    def post(self, request):
        try:
            user = request.user
            answers_data = request.data.get('answers', [])
            
            question_ids = [a.get('question_id') for a in answers_data]
            if len(question_ids) != len(set(question_ids)):
                return Response(
                    {'error': 'Duplicate question_id found in answers.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            assessment = self.assessment_service.get_latest_by_user(user)
            if not assessment:
                return Response(
                    {'error': 'Assessment not found or access denied'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            if not self.assessment_service.is_active(user):
                return Response(
                    {'error': 'Assessment is not active'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not self.assessment_checkin_answer_service.can_checkin_today(assessment):
                return Response(
                    {'error': 'already checked-in'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            checkin_questions = self.question_service.filter(category='check-in', is_active=True)
            checkin_question_ids = set(q.id for q in checkin_questions)
            submitted_question_ids = set(a.get('question_id') for a in answers_data)

            if checkin_question_ids != submitted_question_ids:
                return Response(
                    {'error': 'You must submit answers for all check-in questions.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            checkin_date = timezone.now()
            
            try:
                with transaction.atomic():
                    created_answers = []

                    for index, answer_data in enumerate(answers_data):
                        question_id = answer_data.get('question_id')
                        if not question_id:
                            raise CheckinValidationError(
                                {'error': 'question_id is required for each answer'},
                                status.HTTP_400_BAD_REQUEST
                            )

                        question = self.question_service.get_by_id(question_id)
                        if not question:
                            raise CheckinValidationError(
                                {'error': f'Question with id {question_id} not found'},
                                status.HTTP_404_NOT_FOUND
                            )

                        if question.category != 'check-in':
                            raise CheckinValidationError(
                                {'error': f'Question {question_id} is not a check-in question'},
                                status.HTTP_400_BAD_REQUEST
                            )

                        answer_text = answer_data.get('answer', '')
                        selected_option_id = answer_data.get('selected_option')
                        selected_option = None

                        if selected_option_id:
                            selected_option = self.question_option_service.get_by_id(selected_option_id)
                            if not selected_option or not selected_option.is_active:
                                raise CheckinValidationError(
                                    {'error': f'Selected option with id {selected_option_id} not found or not active'},
                                    status.HTTP_404_NOT_FOUND
                                )

                            try:
                                validation_data = {
                                    'question': question,
                                    'selected_option': selected_option
                                }
                                self.question_option_service.validate(validation_data)
                            except ValueError as e:
                                raise CheckinValidationError(
                                    {'error': str(e)},
                                    status.HTTP_400_BAD_REQUEST
                                )

                        if not answer_text and not selected_option:
                            raise CheckinValidationError(
                                {'error': f'Either answer text or selected_option is required for question {question_id}'},
                                status.HTTP_400_BAD_REQUEST
                            )

                        try:
                            checkin_answer = self.assessment_checkin_answer_service.create(
                                assessment=assessment,
                                question=question,
                                answer=answer_text if answer_text else None,
                                selected_option=selected_option,
                                checkin_date=checkin_date
                            )
                            created_answers.append(checkin_answer)
                        except Exception as e:
                            raise CheckinValidationError(
                                {'error': f'Failed to create answer for question {question_id}: {str(e)}'},
                                status.HTTP_400_BAD_REQUEST
                            )

                assessment.refresh_from_db()
                serializer = AssessmentSerializer(assessment)
                return Response({
                    'message': f'Successfully created {len(created_answers)} check-in answers',
                    'assessment': serializer.data
                }, status=status.HTTP_200_OK)

            except CheckinValidationError as e:
                return Response(e.message, status=e.status_code)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )