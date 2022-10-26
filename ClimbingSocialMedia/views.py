from django.shortcuts import render

from .models import UserProfile

def home(request):
    return render(request, 'ClimbingSocialMedia/home.html')

def posts(request):
    return render(request, 'ClimbingSocialMedia/posts.html')