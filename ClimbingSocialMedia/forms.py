from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

## Form to update user info
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

## Form to update userprofile info
class UpdateProfileForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    facebook_url = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    twitter_url = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    youtube_url = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    instagram_url = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))

    class Meta:
        model = UserProfile
        fields = ['picture', 'bio', 'facebook_url', 'twitter_url', 'youtube_url', 'instagram_url']