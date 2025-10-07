from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from app_offers.models import Offer

from ..api.serializers import OfferDetailSerializer, OffersSerializer
from app_auth.models import UserProfile


class OfferAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        UserProfile.objects.create(user=self.user, type='business')
        self.anotherUser = User.objects.create_user(username='anotheruser', password='testpass')
        UserProfile.objects.create(user=self.anotherUser, type='business')

        # Authenticate the test client
        # self.client = APIClient()
        # self.client.login(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.offers = [
            Offer.objects.create(user=self.user, title='Test Offer', description='This is a test offer.', min_price=100.00, min_delivery_time=5),
            Offer.objects.create(user=self.anotherUser, title='Test Another Offer', description='This is another test offer.', min_price=105.00, min_delivery_time=7)
        ]

        self.offerCount = Offer.objects.all().count()
        
    def test_unauthorized_access(self):
        url = reverse('offers-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.offerCount)

    def test_offer_properties(self):
        offer = self.offers[0]
        url = reverse('offers-detail', kwargs={'pk': offer.id})
        response = self.client.get(url)

        self.assertEqual(response.data['results'][0], {'id': 1, 'title': 'Test Offer', 'description': 'This is a test offer.', 'min_price': '100.00', 'min_delivery_time': 5, 'user': 1, 'image': None, 'created_at': response.data['results'][0]['created_at'], 'updated_at': response.data['results'][0]['updated_at'], 'details': [], 'user_details': {'first_name': '', 'last_name': '', 'username': 'testuser'}})

    

    # def test_get_offers_list(self):
    #     Offer.objects.create(user=self.user, title='Test Offer', description='This is a test offer.', min_price=100.00, min_delivery_time=5)
    #     Offer.objects.create(user=self.user, title='Test Offer', description='This is a test offer.', min_price=100.00, min_delivery_time=5)
    #     url = reverse('offers-list')
    #     response = self.client.get(url)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_create_offer(self):
    #     url = reverse('offers-list')
    #     data = self.offer
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # def test_get_offer_detail(self):
    #     url = reverse('offers-detail', kwargs={'pk': self.offer.id})
    #     response = self.client.get(url)
    #     expected_data = OfferDetailSerializer(self.offer).data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, expected_data)
