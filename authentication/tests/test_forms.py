from django.test import TestCase
from authentication.forms import CreateUserForm, UpdateUserInfo
from authentication.models import UserBlog
from django.urls import reverse

class CreateUserTest(TestCase):
    def dummy_data(self, username='testuser', email='test@test.com', password1='Testpass10', password2='Testpass10'):
        return {
            'username' : username,
            'email' : email,
            'password1' : password1,
            'password2' : password2,
        }

    def generate_response(self, information):
        resp = self.client.post(reverse('register'), data=information)
        return resp

    def test_valid_form(self):
        user_data = self.dummy_data()
        form = CreateUserForm(data=self.dummy_data())
        self.assertTrue(form.is_valid())

    def test_username_min_char_validation(self):
        user_data = self.dummy_data(username='Te')
        resp = self.generate_response(information=user_data)
        self.assertFormError(resp, 'register_form', 'username', "Your username must have at least 3 characters")

    def test_password_upper_validation(self):
        user_data = self.dummy_data(password1='testpass1001', password2='testpass1001')
        resp = self.generate_response(information=user_data)
        self.assertFormError(resp, 'register_form', 'password1', "Your password must contain at least one uppercase letter")

    def test_invalid_email(self):
        user_data = self.dummy_data(email='test.com')
        resp = self.generate_response(information=user_data)
        self.assertFormError(resp, 'register_form', 'email', "Please enter a valid email")

class UpdateUserForm(TestCase):
    def setUp(self):
        user = UserBlog.objects.create(username='testuser', email='test@test.com', password='Testpass10')

    def dummy_data(self, username='testuser2', email='test2@test.com'):
        return {
            'username' : username,
            'email' : email,
        }
    
    def test_update_username(self):
        user_data = self.dummy_data()
        form = UpdateUserInfo(data=user_data)
        self.assertTrue(form.is_valid())