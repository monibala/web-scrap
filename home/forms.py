from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    user_id = forms.CharField(max_length=200, required=True, label="User ID")
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser 
        fields = ('user_id', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
