from django.shortcuts import render
from blog.models import Post, Comment
from authentication.models import UserBlog
from django.utils import dateformat
from django.utils.text import slugify
from django.utils.timezone import activate
from django.db.models import Q
from settings import settings
from authentication.views import logout
from django.forms import inlineformset_factory
from .forms import CreatePostForm, CreateCommentForm, UpdatePostForm
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    LoginRequiredMixin
)
from django.core.exceptions import PermissionDenied

def homepage(request):
    post_list = Post.objects.all()
    context = {
        'post_list' : post_list,
    }
    return render(request,"blog/index.html", context)

def post_archives(request, **kwargs):
    current_post_author = kwargs['user']
    current_post_id = kwargs['id']
    current_post_title = kwargs['title']

    post_list = Post.objects.all()
    comment_list = Comment.objects.all().filter(parent_post=current_post_id, reply_parent=None)

    is_post_url = False
    is_user_post = True if request.user.username == current_post_author else False

    # Filters of post list according to arguments
    if 'user' in kwargs:
        #Filter user posts
        post_list = post_list.filter(Q(author__username__iexact=current_post_author))
    if 'id' in kwargs:
        #Filter individual posts
        post_list = post_list.filter(Q(id=current_post_id))
        post_objects = Post.objects.all()
        if request.method == 'POST':
            if request.user.is_authenticated:
                if request.POST.get('parent_comment'):

                    #Assign reply form
                    reply_form = CreateCommentForm(
                            request.POST,user=request.user, 
                            post=post_objects.get(pk=current_post_id), 
                            parent_comment=request.POST.get('parent_comment')
                        )

                    # Validate and save Reply Form   
                    if reply_form.is_valid():
                        reply_form.save()
                        messages.success(request, "Replied successfully")
                else:

                    #Assign comment form
                    comment_form = CreateCommentForm(request.POST, user=request.user, post=post_objects.get(pk=current_post_id), parent_comment=None)

                    #Validate and save comment Form
                    if comment_form.is_valid():
                        comment_form.save()
                        messages.success(request, "Comment posted successfully")
                return redirect('post_detail', user=current_post_author, id=current_post_id, title=current_post_title)
            else:
                return redirect('/user/login/?next=%s' % request.path)
        else:
            reply_form = CreateCommentForm(user=request.user, post=Post.objects.get(pk=current_post_id))
            comment_form = CreateCommentForm(user=request.user, post=Post.objects.get(pk=current_post_id))
        is_post_url = True

    context = {
        'post_list' : list(post_list),
        'is_post_url' : is_post_url,
        'comment_list' : comment_list,
        'comment_form' : comment_form,
        'reply_form' : reply_form,
    }

    return render(request, "blog/posts_filters.html", context)


@login_required
def create_post(request, **kwargs):
    if request.method == 'POST':
        post_form = CreatePostForm(request.POST, request.FILES, user=request.user)
        if post_form.is_valid():
            post_saved = post_form.save()
            messages.success(request, "Post created successfully")
            return redirect('post_detail', user=request.user, id=post_saved.id, title=post_saved.slug_name())
    else:
        post_form = CreatePostForm(user=request.user)
    return render(request, 'blog/create_post.html', context = {'post_form' : post_form})

class DeletePostView(UserPassesTestMixin, DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class DeleteCommentView(UserPassesTestMixin, DeleteView, LoginRequiredMixin):
    model = Comment
    template_name = 'blog/delete_comment.html'
    success_url = reverse_lazy('homepage')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

def update_post_view(request, *args, **kwargs):
    post_instance = Post.objects.get(pk=kwargs['pk'])
    if request.user == post_instance.author:
        if request.method == 'POST':
            info_form = UpdatePostForm(request.POST, request.FILES, instance=post_instance)

            if info_form.is_valid():
                post = info_form.save(commit=False)
                if request.FILES:
                    post.post_image = request.FILES['post_image']
                post.save()
                messages.success(request, "Post updated successfully")
                return redirect('post_detail', user=post.author, id=post.id, title=slugify(post.title))
        else:
            info_form = UpdatePostForm(instance=post_instance)
    else:
        raise PermissionDenied
    return render(request, 'blog/update_post.html', {'info_form' : info_form, 'object' : post_instance})