from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from .models import Post



def auth_login(request):
    if request.method == "POST": #on form submit
        username = request.POST.get("uname") #get user from input on login page
        psw = request.POST.get("psw") #get password from input on login page
        user = authenticate(request, username=username, password=psw)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect(reverse("Post"))
        else:
            # Could did not authenticate the credentials
            return render(request, 'ClimbingSocialMedia/Login.html')
    return render(request, 'ClimbingSocialMedia/Login.html')

def register(request):
    if request.method == "POST": #on form submit
        email = request.POST.get("email") #get email from input on register page
        username = request.POST.get("uname") #get user from input on register page
        psw = request.POST.get("psw") #get password from input on register page
        user = User.objects.create_user(email=email, username=username, password=psw)
        user.save()
        return redirect(reverse("Post"))
    return render(request, 'ClimbingSocialMedia/Register.html')
def tos(request):
     return render(request, 'ClimbingSocialMedia/TOS.txt')

def posts(request):
    data = Post.objects.all()

    post = {
        "post": data
    }

    return render(request, 'ClimbingSocialMedia/Posts.html', context=post)

def profile(request):
    return render(request, 'ClimbingSocialMedia/ProfilePage.html')

def per_info(request):
    return render(request, 'ClimbingSocialMedia/PersonalInfo.html')