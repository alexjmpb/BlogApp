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
        self.user = UserBlog.objects.create_user(username='Testuser', email='test@testmail.com', password='Test1001')
        self.post = Post.objects.create(author=self.user, title='Test Post Title', content='Content Post Test!')

    def test_homepage_url(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_post_url(self):
        response = self.client.get(self.post.get_abosulte_url())
        self.assertEqual(response.status_code, 200)
    
    def test_user_url(self):
        response = self.client.get(reverse('user_detail', kwargs={'user' : self.user.username}))
        self.assertEqual(response.status_code, 200)
    
    def test_posts_page(self):
        response = self.client.get(reverse('post_detail', kwargs={'user' : self.user.username, 'title' : slugify(self.post.title), 'id' : self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_create_post_get(self):
        self.client.login(username='Testuser', password='Test1001')
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_post_post(self):
        self.client.login(username='Testuser', password='Test1001')
        response = self.client.post(reverse('create_post'), data={'title' : 'Test Post Title 2', 'content' : 'Content Post Test 2'}, follow=True)
        post_created = Post.objects.get(title='Test Post Title 2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(post_created.title, 'Test Post Title 2')
    
    def test_update_post(self):
        self.client.login(username='Testuser', password='Test1001')
        response = self.client.post(reverse('update_post', kwargs={'pk' : self.post.id}), data={'title' : 'Test Post Updated'})
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        self.client.login(username='Testuser', password='Test1001')
        response = self.client.post(reverse('delete_post', kwargs={'pk' : self.post.id}))
        self.assertTrue(len(Post.objects.all()) == 0)
        self.assertEqual(response.status_code, 302)
    