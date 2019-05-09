# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models
from django.contrib.auth.models import User


def get_image_path(instance, filename):
    return os.path.join('static/users/', str(instance.id), filename)

# Create your models here.
class Usuarios(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen_perfil = models.ImageField(upload_to=get_image_path, blank=True, null=True, default='/static'
                                                                                               '/default_profile.png')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Comentarios(models.Model):
    usuario = models.ForeignKey(Usuarios)
    comentario = models.CharField(max_length=500)
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'