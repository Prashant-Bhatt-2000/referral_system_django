from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Referral
import uuid

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Assuming these are the correct URL names for your API endpoints
        self.create_user_url = reverse('create_user')
        self.login_user_url = reverse('login_user')
        self.get_users_url = reverse('get_users')
        self.get_user_by_id_url = reverse('get_user', args=['1'])
        self.referrals_url = reverse('get_user_referrals')

    def test_create_user(self):
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass'}
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        invalid_data = {'username': 'testuser2'}
        response = self.client.post(self.create_user_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

        data = {'email': 'test@example.com', 'password': 'testpass'}
        response = self.client.post(self.login_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        invalid_data = {'email': 'test@example.com', 'password': 'wrongpass'}
        response = self.client.post(self.login_user_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_users(self):
        User.objects.create_user(username='user1', email='user1@example.com', password='userpass1')
        User.objects.create_user(username='user2', email='user2@example.com', password='userpass2')

        self.client.force_authenticate(user=User.objects.first())
        response = self.client.get(self.get_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


    def test_get_user_referrals(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

        self.client.force_authenticate(user=user)
        response = self.client.get(self.referrals_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0) 
