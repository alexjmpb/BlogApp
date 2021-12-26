from django.shortcuts import render
from .models import Post, UserBlog, Comment
from django.utils import dateformat
from django.utils.text import slugify
from django.db.models import Q


def homepage(request):
    context = {
        'logged' : False,
        'post_list' : list(Post.objects.all())
    }
    return render(request,"blog/index.html", context)

def post_archives(request, **kwargs):
    post_list = Post.objects.all()
    if 'user' in kwargs: post_list = post_list.filter(Q(author__username=kwargs['user']))
    if 'id' in kwargs: post_list = post_list.filter(Q(id=kwargs['id']))

    context = {
        'logged' : False,
        'post_list' : list(post_list),
        'comment_list' : Comment.objects.all().filter(parent_post__id=kwargs.get('id'))
    }
    return render(request, "blog/posts_filters.html", context)

def user_blog_view(request, **kwargs):
    username_passed = kwargs.get('user')
    user = UserBlog.objects.get(username=username_passed)

    context = {
        'logged' : False,
        'user' : user,
        'user_posts' : list(Post.objects.all().filter(Q(author__username=kwargs['user'])))
    }

    return render(request, "blog/user_page.html", context)