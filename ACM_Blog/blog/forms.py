from django import forms
from django.contrib.auth.models import User
from .models import Avatar

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model= User
        fields=['username','email','password']
        
class ProfileImageForm(forms.ModelForm):
    profile_image = forms.ImageField()
    class Meta:
        model=Avatar
        fields=['profile_image']
