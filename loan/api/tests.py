from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Loan, Payment
from django.utils import timezone
import numpy as np
import datetime

class LoanPaymentTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        self.loan1 = Loan.objects.create(
            value=5000,
            interest_rate=5.0,
            request_date="2023-09-12T00:00:00Z",
            ip_address="192.168.0.1",
            bank="Test Bank",
            client="John Doe",
            user=self.user1
        )

        self.payment1 = Payment.objects.create(
            date="2023-09-21T00:00:00Z",
            value=500,
            loan=self.loan1,
            user=self.user1
        )

        self.loan2 = Loan.objects.create(
            value=7000,
            interest_rate=4.0,
            request_date="2023-09-22T00:00:00Z",
            ip_address="192.168.0.2",
            bank="Another Bank",
            client="Jane Doe",
            user=self.user2
        )

        self.payment2 = Payment.objects.create(
            date="2023-09-22T00:00:00Z",
            value=7000,
            loan=self.loan2,
            user=self.user2
        )

    def authenticate(self, username: str, password: str):
        url = reverse('token_obtain_pair')
        response = self.client.post(
            url,
            {'username': username, 'password': password},
            format='json'
        )
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_authenticated_user_can_create_loan(self):
        self.authenticate(username='user1', password='password1')

        url = reverse('loan-list')
        data = {
            'value': 10000,
            'interest_rate': 4.5,
            'request_date': "2023-09-30T00:00:00Z",
            'ip_address': "192.168.0.3",
            'bank': "Bank Test",
            'client': "Client Test"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.filter(user=self.user1).count(), 2)

    def test_authenticated_user_can_retrieve_own_loan(self):
        self.authenticate(username='user1', password='password1')

        url = reverse('loan-detail', args=[self.loan1.id])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['loan']['client'], "John Doe")
        self.assertEqual(response.data['loan']['ip_address'], "192.168.0.1")
        self.assertEqual(response.data['loan']['bank'], "Test Bank")
        self.assertEqual(response.data['loan']['request_date'], "2023-09-12T00:00:00Z")
        self.assertEqual(response.data['loan']['interest_rate'], 5.0)
        self.assertEqual(len(response.data['payments']), 1)
        self.assertEqual(response.data['payments'][0]['value'], 500)
        self.assertEqual(response.data['payments'][0]['date'], "2023-09-21T00:00:00Z")

    def test_authenticated_user_cannot_retrieve_other_users_loan(self):
        self.authenticate(username='user1', password='password1')

        url = reverse('loan-detail', args=[self.loan2.id])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_create_payment(self):
        self.authenticate(username='user1', password='password1')

        url = reverse('payment-list')
        data = {
            'date': "2023-10-01T00:00:00Z",
            'value': 600,
            'loan': self.loan1.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.filter(user=self.user1, loan=self.loan1).count(), 2)

    def test_authenticated_user_cannot_create_payment_for_other_users_loan(self):
        self.authenticate(username='user1', password='password1')

        url = reverse('payment-list')
        data = {
            'date': "2023-10-01T00:00:00Z",
            'value': 600,
            'loan': self.loan2.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_still_due_quited_loan(self):
        self.authenticate(username='user2', password='password2')

        url = reverse('loan-detail', args=[self.loan2.id])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['loan']['still_due'], 0)

    def test_still_due_in_progress_loan(self):
        self.authenticate(username='user1', password='password1')

        url = reverse('loan-detail', args=[self.loan1.id])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        loan_date = datetime.datetime.strptime(
            response.data['loan']['request_date'],
            "%Y-%m-%dT%H:%M:%SZ"
        )
        loan_date = timezone.make_aware(loan_date, timezone.get_current_timezone())
        today = timezone.now()
        date_diff = (today - loan_date).days

        loan_value = response.data['loan']['value']
        interest_rate = response.data['loan']['interest_rate']
        payment_value = response.data['payments'][0]['value']
        pro_rata_day = interest_rate / 30 / 100

        max_value = loan_value * np.power(1 + pro_rata_day, date_diff) - payment_value
        min_value = (loan_value - payment_value) * np.power(1 + pro_rata_day, date_diff)

        self.assertGreaterEqual(response.data['loan']['still_due'], min_value)
        self.assertLessEqual(response.data['loan']['still_due'], max_value)

    def test_unauthenticated_user_cannot_access_any_loan(self):
        url = reverse('loan-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_only_sees_their_own_loans_in_list(self):
        self.authenticate(username='user1', password='password1')

        url = reverse('loan-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client'], "John Doe")
