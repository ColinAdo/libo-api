from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser

#  Custom user creation from 
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('profile_picture',)

#  Custom user change/update from 
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields
