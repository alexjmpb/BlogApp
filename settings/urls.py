from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def response_404_handler(request, exception=None):
    return render(request, '404.html')

def response_500_handler(request, exception=None):
    return render(request, '500.html')

def response_403_handler(request, exception=None):
    return render(request, '403.html')

def response_400_handler(request, exception=None):
    return render(request, '400.html')


urlpatterns = [
    path('', include('blog.urls')),
    path('iFoT83Jsr48dBd/', admin.site.urls),
]

handler404 = response_404_handler
handler500 = response_500_handler
handler403 = response_403_handler
handler400 = response_400_handler