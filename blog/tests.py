from django.test import TestCase
from .models import UserBlog, Post, Comment
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import dateformat
from django.utils.text import slugify
from django.urls import reverse


class BlogURLTest(TestCase):
    def test_post_url(self):
        user = UserBlog.objects.create_user(username='Testuser', email='test@testmail.com')
        post = Post.objects.create(author=user, title='Test Post Tile', content='Content Post Test!')
        response = self.client.get(post.get_abosulte_url())
        self.assertEqual(response.status_code, 200)
