from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, TextInput, EmailField, EmailInput, PasswordInput


class RegisterForm(UserCreationForm):
    username = CharField(max_length=100, required=True, widget=TextInput(attrs={"class": "form-control", 'placeholder': 'username'}))
    name = CharField(max_length=150, required=False, widget=TextInput(attrs={"class": "form-control", 'placeholder': 'name'}))
    email = EmailField(max_length=150, required=True, widget=EmailInput(attrs={"class": "form-control", 'placeholder': 'email'}))
    password1 = CharField(max_length=12, min_length=8, required=True,
                          widget=PasswordInput(attrs={"class": "form-control", 'placeholder': 'password'}))
    password2 = CharField(max_length=12, min_length=8, required=True,
                          widget=PasswordInput(attrs={"class": "form-control", 'placeholder': 'confirm password'}))

    class Meta:
        model = User
        fields = ("username", "name", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = CharField(max_length=100, required=True, widget=TextInput(attrs={"class": "form-control", 'placeholder': 'username'}))
    password = CharField(max_length=12, min_length=8, required=True,
                          widget=PasswordInput(attrs={"class": "form-control", 'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ("username", "password")