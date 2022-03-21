from . import views as auth_views
from django.urls import path, include, re_path, reverse, reverse_lazy, resolve
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as builtin_auth_views

urlpatterns = [
    path("register/", auth_views.register_user, name='register'),
    re_path(r"^register/(?:next=(?P<next_path>\w+)/)?$", auth_views.register_user, name='register_next'),
    path("login/", auth_views.login_user, name='login'),
    re_path(r"^login/(?:next=(?P<next_path>\w+)/)?$", auth_views.login, name='login_next'),
    path("logout/", auth_views.logout_user, name='logout'),
    path("password_change/", include([
        path("", auth_views.PasswordChangeView.as_view(template_name='authentication/change_password.html'),name="password_change"), 
        path("done/", auth_views.change_password_done, name="password_change_done")
    ])),
    path("update_user", auth_views.update_user_info, name="update_user_info"),
    path("delete_user/<pk>/", auth_views.DeleteUserView.as_view(), name="delete_user"),

]