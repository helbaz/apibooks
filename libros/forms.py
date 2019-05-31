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
        widgets = {
            'generos': forms.CheckboxSelectMultiple,
        }


class formCapitulo(forms.ModelForm):
    class Meta:
        model = Capitulos
        fields = ('titulo', 'num_capitulo')


class formEditarCapitulo(forms.ModelForm):
    class Meta:
        model = Capitulos
        fields = ('titulo', 'num_capitulo')

        def __init__(self, *args, **kwargs):
            super(formEditarCapitulo, self).__init__(*args, **kwargs)
            self.fields['contenido'].required = True


class formListaCaps(forms.ModelForm):
    class Meta:
        model = Libros
        fields = "__all__"


class formEditarLibro(forms.ModelForm):
    class Meta:
        model = Libros
        fields = ('titulo', 'generos', 'descripcion', 'imagen_perfil')
        widgets = {
            'generos': forms.CheckboxSelectMultiple,
        }
