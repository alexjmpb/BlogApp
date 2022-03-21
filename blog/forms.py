from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from blog.models import Post, Comment
from authentication.models import UserBlog
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.validators import MinLengthValidator

class BasePostForm(forms.ModelForm):
    post_image = forms.ImageField(widget=forms.FileInput(attrs={'onchange' : "previewFile()"}), required=False)
    title = forms.CharField(validators=[MinLengthValidator(8, message=_("The title must have at least 8 characters"))])
    content = forms.CharField(max_length=20000, widget=forms.Textarea(), validators=[MinLengthValidator(8, message=_("The content must have at least 8 characters"))])

    class Meta:
        model = Post
        fields = ('title', 'content', 'post_image')

class CreatePostForm(BasePostForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreatePostForm, self).__init__(*args, **kwargs)

    
    def save(self, commit=True):
        post = super().save(commit=False)
        post.author = self.user

        if commit:
            post.save()
        return post

class CreateCommentForm(forms.ModelForm):
    content = forms.CharField(max_length=2500, widget=forms.Textarea(attrs={'placeholder' : 'Comment something about this'}))
    class Meta:
        model = Comment
        fields = ('content',)
    

    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        self.user = kwargs.pop('user', None)
        self.parent_comment = kwargs.pop('parent_comment', None)
        super(CreateCommentForm, self).__init__(*args, **kwargs)
    

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.parent_post = self.post
        comment.author = self.user
        if self.parent_comment is not None:
            comment.reply_parent = Comment.objects.get(pk=self.parent_comment)
        else:
            comment.reply_parent = None

        if commit:
            comment.save()
        return comment

class UpdatePostForm(BasePostForm):
    def save(self, commit=True):
        post = super().save(commit=False)
        post.author = self.instance.author

        if commit:
            post.save()
        return post