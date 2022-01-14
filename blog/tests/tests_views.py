from django.test import TestCase
from blog.models import Post, Comment
from authentication.models import UserBlog
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import dateformat
from django.utils.text import slugify
from django.urls import reverse
import tempfile

class BlogURLTest(TestCase):
    def setUp(self):
        self.user = UserBlog.objects.create_user(username='Testuser', email='test@testmail.com')
        self.post = Post.objects.create(author=self.user, title='Test Post Tile', content='Content Post Test!')

    def test_homepage_url(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_post_url(self):
        response = self.client.get(self.post.get_abosulte_url())
        self.assertEqual(response.status_code, 200)
    
    def test_user_url(self):
        response = self.client.get(reverse('user_detail', kwargs={'user' : self.user.username}))
        self.assertEqual(response.status_code, 200)
    
    def test_user_posts_test(self):
        response = self.client.get(reverse('user_posts', kwargs={'user' : self.user.username}))
        self.assertEqual(response.status_code, 200)
