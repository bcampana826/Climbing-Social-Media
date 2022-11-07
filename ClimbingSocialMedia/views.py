from django.shortcuts import render

from .models import Post



def login(request):
    return render(request, 'ClimbingSocialMedia/Login.html')
def register(request):
    return render(request, 'ClimbingSocialMedia/Register.html')
def tos(request):
     return render(request, 'ClimbingSocialMedia/TOS.txt')

def posts(request):
    data = Post.objects.all()

    post = {
        "post": data
    }

    if request.method == 'POST':
      if request.POST.get('description'):
            createPost=Post()
            createPost.description = request.POST.get('description')
            createPost.save()
            return render(request, 'ClimbingSocialMedia/Posts.html', context=post)  

    else:
            return render(request,'ClimbingSocialMedia/Posts.html', context=post)
   
    return render(request, 'ClimbingSocialMedia/Posts.html', context=post)
