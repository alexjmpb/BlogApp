from django.shortcuts import render
from blog.models import Post, Comment
from authentication.models import UserBlog
from django.utils import dateformat
from django.utils.text import slugify
from django.utils.timezone import activate
from django.db.models import Q
from settings import settings
from authentication.views import logout


def homepage(request):
    post_list = Post.objects.all()
    context = {
        'post_list' : post_list,
    }
    return render(request,"blog/index.html", context)

def post_archives(request, **kwargs):
    post_list = Post.objects.all()
    comment_list = Comment.objects.all().filter(parent_post=kwargs.get('id'), reply_parent=None)
    is_post_url = False
    # Filters of post list according to arguments
    if 'user' in kwargs:
        post_list = post_list.filter(Q(author__username__iexact=kwargs['user']))
    if 'id' in kwargs:
        post_list = post_list.filter(Q(id=kwargs['id']))
        is_post_url = True

    context = {
        'post_list' : list(post_list),
        'is_post_url' : is_post_url,
        'comment_list' : comment_list,

    }
    return render(request, "blog/posts_filters.html", context)