from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

## Recieves signal if a new user is created, then creates a userprofile for that user
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

## Once user creates user profile, profile is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()
