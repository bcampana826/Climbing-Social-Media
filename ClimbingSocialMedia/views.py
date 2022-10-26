from django.shortcuts import render

from .models import Post


def home(request):
    return render(request, 'ClimbingSocialMedia/home.html')


def posts(request):
    data = Post.objects.all()[0]

    post = {
        "post": data
    }

    return render(request, 'ClimbingSocialMedia/posts.html', context=post)
