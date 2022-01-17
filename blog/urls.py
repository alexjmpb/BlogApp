from . import views
from django.urls import path, include, re_path
from authentication import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("user/", include([
        path("", include("authentication.urls")),
        path("<str:user>/", include([
            path("posts/", include([
                path("", views.post_archives, name='user_posts'),
                path("<int:id>-<slug:title>/", views.post_archives, name='post_detail'),
            ])),
            path("", auth_views.user_blog_view, name='user_detail'),
        ])),
    ])),
    path("create_post", views.create_post, name='create_post'),
    path('delete_post/<pk>', views.DeletePostView.as_view(), name='delete_post'),
    path('delete_comment/<pk>', views.DeleteCommentView.as_view(), name='delete_comment'),
    path("update_post/<pk>/", views.update_post_view, name='update_post')    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
