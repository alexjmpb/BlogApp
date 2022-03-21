from django.test import TestCase
from authentication.models import UserBlog
from django.contrib.auth.hashers import check_password

class UserModelTest(TestCase):
    def setUp(self):
        self.user = UserBlog.objects.create_user(username='Testuser', email='test@testmail.com')
        self.user.set_password('Testpass')

    def test_user(self):
        self.assertEqual(self.user.username, 'Testuser')
        self.assertEqual(self.user.email, 'test@testmail.com')
        self.assertEqual(check_password('Testpass', self.user.password), True)