from dataclasses import fields
from socket import fromshare
from django import forms
from django.contrib.auth.forms import UserCreationForm      # importacion de comandos para crar formulario de usuario basico
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