from django.db import models
from authentication.models import UserBlog
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone, dateformat
from django.utils.text import slugify
from django.urls import reverse
import os
import datetime
from PIL import Image

def posts_images_path(instance, filename):
    return f'posts/images/{instance.author.username}/{instance.id}/{filename}'
    
class Post(models.Model):
    title = models.CharField(max_length=60)
    author = models.ForeignKey(UserBlog, on_delete=models.CASCADE)
    content = models.TextField()
    time_posted = models.DateTimeField(default=timezone.now)
    post_image = models.ImageField(upload_to=posts_images_path, blank=True)


    def slug_name(self):
        return slugify(self.title)


    def get_abosulte_url(self):
        return reverse('post_detail',kwargs={'user' : self.author.username,'title' : self.slug_name(),'id' : self.id})


    def __str__(self):
        return self.title

    
    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.post_image:
            img = Image.open(self.post_image.path)

            if img.height > 800 or img.width > 800:
                size = (800, 800)
                img.thumbnail(size)
                img.save(self.post_image.path)

class Comment(models.Model):
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(UserBlog, on_delete=models.CASCADE)
    reply_parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    content = models.TextField()
    time_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.content[0:9]
