from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from django.forms import ModelForm
from .models import Userinfo

class CreateUserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email',  'password1' , 'password2']

class userinfoform(ModelForm):
    class Meta:
        model = Userinfo
        exclude = ['user' , 'sentotp','phoneverified']