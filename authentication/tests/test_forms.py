from django.test import TestCase
from authentication.forms import CreateUserForm
from authentication.models import UserBlog
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.urls import reverse
from authentication.views import register_user
from django.contrib.auth.hashers import make_password

import tempfile

class CreateUserTest(TestCase):
    def dummy_data(self, username='testuser', email='test@test.com', password1='Testpass10', password2='Testpass10'):
        return {
            'username' : username,
            'email' : email,
            'password1' : password1,
            'password2' : password2,
        }

    def generate_response(self, information):
        rqst = reverse('register')
        resp = self.client.post(rqst, data=information)
        form = resp.context['form']

        return rqst, resp, form

    def test_valid_form(self):
        user_data = self.dummy_data()
        form = CreateUserForm(data=user_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_username_min_char_validation(self):
        user_data = self.dummy_data(username='Te')
        rqst, resp, form = self.generate_response(information=user_data)
        self.assertFormError(resp, 'form', 'username', "Your username must have at least 3 characters")

    def test_password_upper_validation(self):
        user_data = self.dummy_data(password1='testpass1001', password2='testpass1001')
        rqst, resp, form = self.generate_response(information=user_data)
        self.assertFormError(resp, 'form', 'password1', "Your password must contain at least one uppercase letter")

    def test_invalid_email(self):
        user_data = self.dummy_data(email='test.com')
        rqst, resp, form = self.generate_response(information=user_data)
        self.assertFormError(resp, 'form', 'email', "Please enter a valid email")