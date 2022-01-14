from django.shortcuts import render, redirect
from django.urls import reverse, resolve, reverse_lazy
from .forms import CreateUserForm, UpdateUserInfo, UserImageForm
from django.contrib.auth.forms import AuthenticationForm
from .models import UserBlog
from blog.models import Post
from django.contrib.auth import views as builtin_auth_views
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin

def register_user(request, *kwargs):
    if request.method == "POST":
        register_form = CreateUserForm(request.POST)
        image_form = UserImageForm(request.POST, request.FILES)

        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            if request.FILES:
                new_user.user_image = request.FILES['user_image']
            new_user.save()
            user_auth = authenticate(
                    request, 
                    username=request.POST['username'], 
                    password=request.POST['password1']
                )
            if user_auth is not None:
                login(request, user_auth)
                if request.POST.get('next') is not None:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('homepage')
            else:
                return redirect(reverse('register'))
    else:
        register_form = CreateUserForm()
        image_form = UserImageForm(request.POST, request.FILES)
    if not request.user.is_authenticated:
        return render(request, "authentication/register.html", context={'register_form' : register_form, 'image_form' : image_form})
    else:
        return redirect('homepage')

def login_user(request, *kwargs):
    if request.method == "POST":
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user_auth = authenticate(
                    request, 
                    username=request.POST['username'], 
                    password=request.POST['password']
                )
            if user_auth is not None:
                login(request, user_auth)
                if request.POST.get('next') is not None:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('homepage')
            else:
                pass
    else:
        login_form = AuthenticationForm()
    if not request.user.is_authenticated:
        return render(request, "authentication/login.html", context={'login_form':login_form})
    else:
        return redirect('homepage')
    
@login_required
def logout_user(request):
    logout(request)
    return redirect('homepage')

def user_blog_view(request, **kwargs):
    username_passed = kwargs.get('user')
    user = UserBlog.objects.get(username__iexact=username_passed)
    post_list = Post.objects.all().filter(author_id=user.id)

    is_user = False
    if user == request.user: is_user = True

    context = {
        'user' : user,
        'post_list' : list(post_list),
        'is_user' : is_user
    }

    return render(request, "authentication/user_page.html", context)

class PasswordChangeView(SuccessMessageMixin, builtin_auth_views.PasswordChangeView):
    success_message = "Password updated successfully"
    success_url = reverse_lazy('password_change_done')

@login_required
def change_password_done(request, **kwargs):
    return redirect('user_detail', user=request.user.username)

@login_required
def update_user_info(request, **kwargs):
    user_instance = UserBlog.objects.get(pk=request.user.id)
    if request.method == 'POST':
        info_form = UpdateUserInfo(request.POST, instance=user_instance)
        image_form = UserImageForm(request.POST, request.FILES)

        if info_form.is_valid() and image_form.is_valid():
            user = info_form.save(commit=False)
            if request.FILES:
                user.user_image = request.FILES['user_image']
            user.save()
            messages.success(request, "Information updated successfully")
            return redirect('user_detail', user=user)
    else:
        info_form = UpdateUserInfo(instance=user_instance)
        image_form = UserImageForm()
    return render(request, 'authentication/update_user.html', {'info_form' : info_form, 'image_form' : image_form})