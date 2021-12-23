from .views import homepage, individual_post
from django.urls import path

urlpatterns = [
    path("", homepage, name='homepage'),
    path('posts/<int:year>/<str:user>/<slug:title>/<int:post_id>', individual_post, name='post_detail')
]
