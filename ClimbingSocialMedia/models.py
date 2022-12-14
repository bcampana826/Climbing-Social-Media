# Do NOT change without confirming with team
import uuid

from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)
    picture = models.ImageField(default='defaultProfilePic.jpg', upload_to='user_profile_pictures', null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    youtube_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    followed_by = models.ManyToManyField(User, related_name="user_followed_by", blank=True)
    following = models.ManyToManyField(User, related_name="user_following", blank=True)
    def __str__(self):
        return f'{self.user.username}\'s Personal Profile'
    ## Resizes the profile picture to 500x500 pixels, so big size images dont take a lot of space.
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.picture.path)

        if img.height > 500 or img.width > 500:
            new_img = (500, 500)
            img.thumbnail(new_img)
            img.save(self.picture.path)
  

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="comment_likes_users", blank=True)
    replies = models.ManyToManyField('self', symmetrical=False)
    description = models.CharField(max_length=500)
    media = models.ImageField(upload_to='', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="post_likes_users", blank=True)
    comments = models.ManyToManyField(Comment, related_name="post_comments_users", blank=True)
    description = models.CharField(max_length=500)
    media = models.ImageField(upload_to='', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
