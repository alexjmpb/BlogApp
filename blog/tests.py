from django.test import TestCase
from .models import UserBlog, Post, Comment
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class BlogTests(TestCase):

    def setUp(self):
        self.user = UserBlog.objects.create_user(
            username = 'Testuser',
            email = 'testemail@email.com',
            password = make_password('Password123')
        )

        self.post = Post.objects.create(
            title = 'Post test',
            content = 'Post content test',
            author = self.user
        )

        self.comment = Comment.objects.create(
            content = 'Comment test',
            parent_post = self.post,
            author = self.user
        )
    
    def test_user(self):
        self.assertEqual(f'{self.user.username}', 'Testuser')
        self.assertEqual(f'{self.user.email}', 'testemail@email.com')
        self.assertFalse(self.user.is_admin)

    def test_post(self):
        self.assertEqual(f'{self.post.title}', 'Post test')
        self.assertEqual(f'{self.post.content}', 'Post content test')
        print(self.post.author)
        print(self.post.title)
        print(self.post.content)
        print(self.post.url())

    def test_comment(self):
            self.assertEqual(f'{self.comment.content}', 'Comment test')
            print(self.comment.parent_post)
            print(self.comment.author)
            print(self.comment.content)

    