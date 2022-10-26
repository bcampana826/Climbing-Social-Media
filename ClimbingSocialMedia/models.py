# Do NOT change without confirming with team

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    picture = models.URLField()


class GymProfile(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    gym_name = models.CharField(max_length=50, null=False)
    bio = models.CharField(max_length=500)
    picture = models.URLField()
    verified = models.BooleanField()
    location = models.CharField(max_length=50)


class Comment(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="comment_likes_users")
    replies = models.ManyToManyField('self', symmetrical=False)
    description = models.CharField(max_length=500)
    media = models.URLField()
    date = models.DateTimeField(auto_now=True)


class Post(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="post_likes_users", blank=True)
    comments = models.ManyToManyField(Comment, related_name="post_comments_users", blank=True)
    description = models.CharField(max_length=500)
    media = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
