import json
from venv import create
from xml.etree.ElementTree import Comment
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import UpdateUserForm, UpdateProfileForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login'))

def auth_login(request):
    if request.method == "POST":  # on form submit
        username = request.POST.get("uname")  # get user from input on login page
        psw = request.POST.get("psw")  # get password from input on login page
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
    if request.method == "POST":  # on form submit
        email = request.POST.get("email")  # get email from input on register page
        username = request.POST.get("uname")  # get user from input on register page
        psw = request.POST.get("psw")  # get password from input on register page
        user = User.objects.create_user(email=email, username=username, password=psw)
        user.save()
        return redirect(reverse("Post"))
    return render(request, 'ClimbingSocialMedia/Register.html')


def tos(request):
    return render(request, 'ClimbingSocialMedia/TOS.txt')

def report(request):
    return render(request, 'ClimbingSocialMedia/Report.html')

@login_required
def posts(request):
    data = Post.objects.all().order_by('-date')  # orders the post being pulled by date
    post = {
        "post": data,  # list of posts pushed to frontend
        "user": request.user

    }

    if request.method == 'POST':  # on form submit
        if request.POST.get('description'):

            createPost = Post()  # creates a new post in databse
            if request.FILES:
                upload = request.FILES['filename']
                fss = FileSystemStorage()
                file = fss.save(upload.name, upload)
                file_url = fss.url(file)
                createPost.media = file_url  # fills in image url fromfrontend

            createPost.description = request.POST.get('description')  # fil's in description field from frontend

            createPost.author = request.user  # grabs current urser and updates author field
            createPost.save()  # saves and updates databse
            return redirect(
                "/post")  # redirects back to page so it doesnt auto fill form and reupload to database on refresh

        if request.POST.get('comment-descr'):
            createComment = Comment()  # creates a new post in databse
            createComment.description = request.POST.get('comment-descr')  # fill's in description field from frontend
            createComment.author = request.user  # grabs current urser and updates author field
            createComment.save()  # saves and updates database
            id = uuid.UUID(request.POST.get('post-id'))
            new_post = Post.objects.get(id=id)
            new_post.comments.add(createComment)
            new_post.save()

            return redirect(
                "/post")  # redirects back to page so it doesnt auto fill form and reupload to database on refresh

    else:
        return render(request, 'ClimbingSocialMedia/Posts.html', context=post)

    return render(request, 'ClimbingSocialMedia/Posts.html', context=post)

@login_required
def profile(request):
    return render(request, 'ClimbingSocialMedia/ProfilePage.html')

def profile_other(request, username): #see a different persons profile
    users = list(User.objects.filter(username=username)) #get the user from path parameter (username)
    if len(users) is 0: #if no user exists with this name
        return HttpResponseRedirect(reverse('Post'))
    user = users[0] #get the user with that username
    if user.username == request.user.username:
        return HttpResponseRedirect(reverse('Profile'))
    return render(request, 'ClimbingSocialMedia/ProfilePage.html', {"user":user, "other":True, "me": request.user})

@login_required
def per_info(request):
    if request.method == 'POST':  # on form submit
        user_form = UpdateUserForm(request.POST, instance=request.user) # update user fields (username or email)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.userprofile) # update userprofile fields

        if user_form.is_valid() and profile_form.is_valid(): # If both user AND profile form instances is valid
            user_form.save() # saves updated user fields
            profile_form.save() # saves updated userprofile fields
            return redirect(to='PersonalInfo') # goes back to info page
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.userprofile)

    return render(request, 'ClimbingSocialMedia/PersonalInfo.html', {'user_form': user_form, 'profile_form': profile_form})

@csrf_exempt
def update_post_likes(request):
    if request.method == 'POST':
        post = json.loads(request.body)
        user = post['user']
        post_id = post['post_id']
        like = post['like']
        # post_id = int(post_id)
        post = Post.objects.get(id=post['post_id'])
        user = User.objects.get(username=user)
        if like is True:
            post.likes.add(user)
        if like is False:
            post.likes.remove(user)
        return HttpResponse("Success")

@csrf_exempt
def update_followers(request):
    if request.method == 'POST':
        post = json.loads(request.body)
        user = post['followed_user'] #user to be followed
        me = post['me'] #the user who is doing the following
        unfollow = post['unfollow'] #boolean  either unfollow (remove) or follow (add)
        user = list(User.objects.filter(username=user))[0]
        followed_user_profile = list(UserProfile.objects.filter(user=user))[0]
        me = list(User.objects.filter(username=me))[0]
        my_profile = list(UserProfile.objects.filter(user=me))[0]
        if unfollow:
            followed_user_profile.followed_by.remove(me)
            my_profile.following.remove(user)
        else:
            followed_user_profile.followed_by.add(me)
            my_profile.following.add(user)
        return HttpResponse("Success")