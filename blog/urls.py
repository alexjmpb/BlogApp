from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("user/<str:user>/", include([
        path("posts/", include([
            path("", views.post_archives, name='user_posts'),
            path("<int:id>-<slug:title>/", views.post_archives, name='post_detail'),
        ])),
        path("", views.user_blog_view, name='user_detail'),
    ]))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
