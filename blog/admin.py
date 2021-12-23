from django.contrib import admin
from .models import UserBlog, Post, Comment

admin.site.register(UserBlog)
admin.site.register(Post)
admin.site.register(Comment)
