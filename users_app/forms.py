from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField()
    FirstName = forms.CharField()
    LastName = forms.CharField()
    
    class Meta:
        model = User
        fields = ['username','email','FirstName','LastName','password1','password2']