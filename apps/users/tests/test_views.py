from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User


class UsernameLoginViewTests(TestCase):
    
    fixtures = ['users.json']
    
    def setup(self):
        self.client = Client()
        self.user = User.objects.get(
            username='sogol123',
        )
        
    def test_GET_login_view(self):
        response = self.client.get(reverse('users:login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'username_login.html')

    def test_POST_login_view(self):
        response = self.client.post(
            reverse('users:login'),
            {
             'username': 'sogol123',
             'password': '321logoss',
            }
        )
        
        self.assertEqual(response.status_code, 200)


class EmailLoginViewTests(TestCase):
    
    fixtures = ['users.json']
    
    def setup(self):
        self.client = Client()
        self.user = User.objects.get(
            username='sogol123',
        )
        
    def test_GET_login_view(self):
        response = self.client.get(reverse('users:email'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email_login.html')
        
    def test_POST_login_view(self):
        response = self.client.post(
            reverse('users:email'),
            {
             'email': 'sogi@customer.test',
            }
        )
        
        self.assertEqual(response.status_code, 302)
    
class OTPViewTests(TestCase):
    
    fixtures = ['users.json']
    
    def setup(self):
        self.client = Client()
        self.user = User.objects.get(
            username='sogol123',
        )
        
    def test_GET_login_view(self):
        response = self.client.get(reverse('users:otp'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'otp.html')
        
    def test_POST_login_view(self):
        response = self.client.post(
            reverse('users:otp'),
        )
        
        self.assertEqual(response.status_code, 200)
        
        
class SignupViewTests(TestCase):
    
    fixtures = ['users.json']
    
    def setup(self):
        self.client = Client()
        self.user = User.objects.get(
            username='sogol123',
        )
        
    def test_GET_login_view(self):
        response = self.client.get(reverse('users:signup'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
    def test_POST_login_view(self):
        response = self.client.post(
            reverse('users:signup'),
        )
        
        self.assertEqual(response.status_code, 200)


class CustomLogoutViewTests(TestCase):
    
    fixtures = ['users.json']
    
    def setup(self):
        self.client = Client()
        self.user = User.objects.get(
            username='sogol123',
        )
        
    def test_GET_login_view(self):
        response = self.client.get(reverse('users:logout'))
        
        self.assertEqual(response.status_code, 302)
        
    def test_POST_login_view(self):
        response = self.client.post(
            reverse('users:logout'),
        )
        
        self.assertEqual(response.status_code, 302)
