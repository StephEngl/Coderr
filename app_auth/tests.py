from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class OfferAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.first_name = 'Test'
        self.user.last_name = 'User'
        self.user.save()
        
        # Authenticate the test client
        self.client.login(username='testuser', password='testpass')

    def get_offers_list(self):
        url = reverse('offer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)