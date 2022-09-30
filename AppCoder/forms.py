from dataclasses import fields
from socket import fromshare
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm      # importacion de comandos para crar formulario de usuario basico
from django.contrib.auth.models import User                 # importacion de comandos para crar formulario de usuario basico


class form_estudiantes(forms.Form):
    nombre = forms.CharField(max_length=30)
    apellido = forms.CharField(max_length=30)
    email = forms.EmailField()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Password", widget= forms.PasswordInput)
    password2 = forms.CharField(label="Repetir Password", widget= forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_text = {k:"" for k in fields}


class UserEditForm(UserChangeForm):
    username = forms.CharField(widget= forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget= forms.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(widget= forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget= forms.TextInput(attrs={'placeholder': 'Last Name'}))
    password = forms.CharField(widget= forms.PasswordInput(attrs={'placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        help_texts = {k:"" for k in fields}


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="", widget= forms.PasswordInput(attrs={'placeholder': "Old Password", }))
    new_password1 = forms.CharField(label="",widget= forms.PasswordInput(attrs={'placeholder': "New password"}))
    new_password2 = forms.CharField(label="",widget= forms.PasswordInput(attrs={'placeholder': "Confirm new password"}))
    class Meta:         # se usa meta cuando se cae encima de variables existentes
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        help_texts = {k:"" for k in fields}


class AvatarFormulario(forms.Form):
    avatar = forms.ImageField()
    