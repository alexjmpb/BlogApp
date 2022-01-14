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
    # path("user/<str:user>/", include([
    #     path("posts/", include([
    #         path("", views.post_archives, name='user_posts'),
    #         path("<int:id>-<slug:title>/", views.post_archives, name='post_detail'),
    #     ])),
    #     path("", views.user_blog_view, name='user_detail'),
    # ])),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
