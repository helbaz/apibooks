# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models
from libros.models import *
from django.contrib.auth.models import User


def get_image_path(instance, filename):
    return os.path.join('static/users/', str(instance.id), filename)

# Create your models here.
class Usuarios(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=False, null=False, unique=True)
    imagen_perfil = models.ImageField(upload_to=get_image_path, blank=True, null=True, default='static'
                                                                                               '/default_profile.png')

    def __unicode__(self):
        return self.usuario.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Comentarios(models.Model):
    usuario = models.ForeignKey(Usuarios)
    #capitulo = models.ForeignKey(Capitulos, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=500)
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'