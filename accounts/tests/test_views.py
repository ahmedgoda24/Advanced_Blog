from django.test import TestCase , Client ,RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .views import signup

class SignUpViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_signup_get(self):
        request = self.factory.get('/signup/')
        response = signup(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertTrue(isinstance(response.context['form'], UserCreationForm))

    def test_signup_post_valid_form(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        request = self.factory.post('/signup/', data)
        response = signup(request)
        self.assertEqual(response.status_code, 200)  # Should redirect
        self.assertEqual(response.url, '/accounts/profile/')  # Check redirection URL
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Check user creation

    def test_signup_post_invalid_form(self):
        data = {}  # Invalid form data, missing required fields
        request = self.factory.post('/signup/', data)
        response = signup(request)
        self.assertEqual(response.status_code, 200)  # Should stay on the signup page
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertFalse(User.objects.filter(username='testuser').exists())  # Ensure no user is create

class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
          # Check if a profile already exists for the user
        self.profile, created = Profile.objects.get_or_create(user=self.user, defaults={'bio': 'Test bio'})
    def test_profile_view(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

  

