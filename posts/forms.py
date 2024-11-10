from . import models
from django import forms
from .models import UserProfile

class createPost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['banner', 'body']
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']