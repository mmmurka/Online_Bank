from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Account


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.account = Account.objects.create(user=self.user)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/home.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/signup.html')

    def test_user_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/login.html')

    def test_success_account_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('success_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking/signup_done.html')




