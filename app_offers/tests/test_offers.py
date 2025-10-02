from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class OfferAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.first_name = 'Test'
        self.user.last_name = 'User'
        self.user.save()
        
        # Authenticate the test client
        self.client.login(username='testuser', password='testpass')

    def test_get_offers_list(self):
        url = reverse('offers-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_request_invalid_min_price(self):
        url = reverse('offers-list')
        # Übergib z. B. einen ungültigen Typ für min_price (String statt float)
        response = self.client.get(url, {'min_price': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn('min_price', response.data)

    def test_bad_request_invalid_ordering(self):
        url = reverse('offers-list')
        # Übergib einen ungültigen Wert für ordering
        response = self.client.get(url, {'ordering': 'invalid_field'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Optionale tiefergehende Prüfung:
        # self.assertIn('ordering', response.data)