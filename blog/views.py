from django.shortcuts import render


def homepage(request):
    return render(request, "blog/index.html", {'logged' : True, 'username' : "John Doe"})