# Do NOT change without confirming with team

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)
    picture = models.ImageField(upload_to='', null=True,blank=True)


class GymProfile(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    gym_name = models.CharField(max_length=50, null=False)
    bio = models.CharField(max_length=500, blank=True)
    picture = models.ImageField(upload_to='', null=True,blank=True)
    verified = models.BooleanField(default=False)
    location = models.CharField(max_length=50, blank=True)


class Comment(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="comment_likes_users", blank=True)
    replies = models.ManyToManyField('self', symmetrical=False)
    description = models.CharField(max_length=500)
    media = models.ImageField(upload_to='', null=True,blank=True)
    date = models.DateTimeField(auto_now=True)


class Post(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="post_likes_users", blank=True)
    comments = models.ManyToManyField(Comment, related_name="post_comments_users", blank=True)
    description = models.CharField(max_length=500)
    media = models.ImageField(upload_to='',null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
