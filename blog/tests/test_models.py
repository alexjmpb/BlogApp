from django.test import TestCase
from blog.models import Post, Comment
from authentication.models import UserBlog
from django.utils.text import slugify
from django.urls import reverse

class BlogModelsTest(TestCase):

    def setUp(self):
        self.user = UserBlog.objects.create_user(username='Testuser', email='test@testmail.com')
        self.user.set_password('Testpass')
        self.post = Post.objects.create(title='Post Test', content='Post content test', author=self.user)
        self.comment = Comment.objects.create(author=self.user, parent_post=self.post, content='Comment Post Test')
        self.reply = Comment.objects.create(author=self.user, parent_post=self.post, reply_parent=self.comment, content='Reply Post Test')

    def test_post(self):
        self.assertEqual(self.post.author.username, 'Testuser')
        self.assertEqual(self.post.title, 'Post Test')
        self.assertEqual(self.post.content, 'Post content test')

    def test_comment(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.parent_post, self.post)
        self.assertEqual(self.comment.reply_parent, None)
        self.assertEqual(self.comment.content, 'Comment Post Test')

    def test_comment(self):
        self.assertEqual(self.reply.author, self.user)
        self.assertEqual(self.reply.parent_post, self.post)
        self.assertEqual(self.reply.reply_parent, self.comment)
        self.assertEqual(self.reply.content, 'Reply Post Test')

