from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.users.models.user_model import User
from unittest.mock import patch
import json

class UserViewTestCase(APITestCase):
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'sex': 'male'
        }
        self.create_url = '/api/accounts/'
        
    @patch('django.core.mail.send_mail')
    def test_create_user_success(self, mock_send_mail):
        mock_send_mail.return_value = True
        
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'User created successfully')
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        
        user = User.objects.get(email=self.user_data['email'])
        self.assertIsNotNone(user)
        self.assertFalse(user.is_verified)
        self.assertIsNotNone(user.verification_code)