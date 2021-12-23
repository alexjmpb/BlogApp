from django.shortcuts import render
from .models import Post, UserBlog
from django.utils import dateformat


def homepage(request):
    context = {
        'logged' : False,
        'post_list' : list(Post.objects.all())
    }
    return render(request,"blog/index.html", context)

def individual_post(request, **kwargs):
    context = {
        'logged' : False,
        'post' : Post.objects.get(id=kwargs.get('post_id'))
    }
    return render(
        request,
        "blog/individual_posts.html", 
        context
    )