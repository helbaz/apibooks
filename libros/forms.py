from fileinput import FileInput

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *


class formPublicar(forms.ModelForm):
    class Meta:
        model = Libros
        fields = ('titulo', 'descripcion', 'generos', 'imagen_perfil')
        # widgets = {
        #     'generos': forms.CheckboxSelectMultiple,
        # }