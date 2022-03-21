from django.test import TestCase
from authentication.models import UserBlog
from blog.models import Post, Comment
from django.urls import reverse
from blog.forms import CreatePostForm, CreateCommentForm, UpdatePostForm

class BlogFormTest(TestCase):
    def setUp(self):
        self.user = UserBlog.objects.create(username='testuser', email='test@test.com', password='Test1001')
        self.post = Post.objects.create(title='Post Title Test', content='Post Content Test', author=self.user)
        self.comment = Comment.objects.create(content='Comment Content Test', author=self.user, parent_post=self.post)

    def test_post_form_valid(self):
        form = CreatePostForm(data={'title' : 'Post Title Test 2', 'content' : 'Post Content Test 2', 'author' : self.user})
        self.assertTrue(form.is_valid())

    def test_update_post_form_valid(self):
        form = UpdatePostForm(data={'title' : 'Post Title Test 2', 'content' : 'Post Content Test 2', 'author' : self.user}, instance=self.post)
        self.assertTrue(form.is_valid())
        self.assertEqual(self.post.title, 'Post Title Test 2')

    def test_comment_form_valid(self):
        form = CreateCommentForm(data={'content' : 'Comment Content Test 2', 'author' : self.user, 'parent_post' : self.post})
        self.assertTrue(form.is_valid())

    def test_reply_form_valid(self):
        form = CreateCommentForm(data={'content' : 'Reply Content Test 2', 'author' : self.user, 'parent_post' : self.post, 'reply_parent' : self.comment})
        self.assertTrue(form.is_valid())
    
