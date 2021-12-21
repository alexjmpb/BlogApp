from .views import homepage
from django.urls import path

urlpatterns = [
    path("", homepage, name='homepage')
]
