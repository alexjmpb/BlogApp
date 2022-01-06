from django.shortcuts import render
from .models import Post, UserBlog, Comment
from django.utils import dateformat
from django.utils.text import slugify
from django.db.models import Q


def homepage(request):
    post_list = Post.objects.all()
    context = {
        'logged' : False,
        'post_list' : post_list,
    }
    return render(request,"blog/index.html", context)

def post_archives(request, **kwargs):
    post_list = Post.objects.all()
    comment_list = Comment.objects.all().filter(parent_post=kwargs.get('id'), reply_parent=None)
    is_post_url = False
    if 'user' in kwargs: post_list = post_list.filter(Q(author__username=kwargs['user']))
    if 'id' in kwargs:
        post_list = post_list.filter(Q(id=kwargs['id']))
        is_post_url = True

    context = {
        'logged' : False,
        'post_list' : list(post_list),
        'is_post_url' : is_post_url,
        'comment_list' : comment_list
    }
    return render(request, "blog/posts_filters.html", context)

def user_blog_view(request, **kwargs):
    username_passed = kwargs.get('user')
    user = UserBlog.objects.get(username=username_passed)
    post_list = Post.objects.all().filter(author_id=user.id)

    context = {
        'logged' : False,
        'user' : user,
        'post_list' : list(post_list)
    }

    return render(request, "blog/user_page.html", context)