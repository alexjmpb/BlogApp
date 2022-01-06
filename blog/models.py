from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone, dateformat
from django.utils.text import slugify
from django.urls import reverse
import os
import datetime


def user_images_path(instance, filename):
    return f'users/images/{instance.username}/{filename}'

def posts_images_path(instance, filename):
    return f'posts/images/{instance.author.username}/{instance.id}/{filename}'

class UserBlogManager(BaseUserManager):
    
    def create_user(self, username, email, password=None, **other_fields):
        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **other_fields):
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_admin') is not True:
            raise ValueError("This user must be admin")

        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBlog(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserBlogManager()
    user_image = models.ImageField(upload_to=user_images_path, default='users/default_user.jpg')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username
    
class Post(models.Model):
    title = models.CharField(max_length=60)
    author = models.ForeignKey(UserBlog, on_delete=models.CASCADE)
    content = models.TextField()
    # dattime.datetime YYMMDD HH:mm:ss:ms tzinfo
    time_posted = models.DateTimeField(default=timezone.now)
    post_image = models.ImageField(upload_to=posts_images_path, blank=True)

    def slug_name(self):
        return slugify(self.title)

    #separate dates for time posted
    def post_date(self):
        year = dateformat.format(self.time_posted, 'Y')
        month = dateformat.format(self.time_posted, 'm')
        day = dateformat.format(self.time_posted, 'd')

    def get_abosulte_url(self):
        return reverse('post_detail',kwargs={'user' : self.author.username,'title' : self.slug_name(),'id' : self.id})

    def __str__(self):
        return self.title

class Comment(models.Model):
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(UserBlog, on_delete=models.CASCADE)
    reply_parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    content = models.TextField()
    time_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content[0:9]

