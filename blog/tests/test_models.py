from django.test import TestCase
from blog.models import UserBlog, Post, Comment
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import dateformat
from django.utils.text import slugify
from django.urls import reverse
import tempfile

class BlogModelsTest(TestCase):

    def setUp(self):
        self.post_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.user = UserBlog.objects.create_user(username='Testuser', email='test@testmail.com')
        self.user.set_password('Testpass')
        self.post = Post.objects.create(title='Post Test', content='Post content test', author=self.user, post_image=self.post_image)

    
    def test_post(self):
        self.assertEqual(self.post.author.username, 'Testuser')
        self.assertEqual(self.post.title, 'Post Test')
        self.assertEqual(self.post.content, 'Post content test')
        self.assertEqual(self.post.post_image, self.post_image)
        self.assertEqual(self.user.user_image, self.user_image)
        print(self.post.post_image.url)

    def test_user(self):
        self.assertEqual(self.user.username, 'Testuser')
        self.assertEqual(self.user.email, 'test@testmail.com')
        self.assertEqual(check_password('Testpass', self.user.password), True)
