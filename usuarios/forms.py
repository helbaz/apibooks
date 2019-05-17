from fileinput import FileInput

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import *

class formRegistre(UserCreationForm):
    nickname = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(formRegistre, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['nickname'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        nNickname = Usuarios.objects.filter(nickname=nickname).count()
        if nNickname > 0:
            raise ValidationError(u"""Aquest nom d'usuari ja existeix""")
        return nickname


class formPerfil(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ('nickname', 'imagen_perfil')

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        instance = getattr(self, 'instance', None)
        nNickname = Usuarios.objects.filter(nickname=nickname).exclude(pk=instance.pk).count()
        if nNickname > 0:
            raise ValidationError(u"""Aquest nom d'usuari ja existeix""")
        return nickname