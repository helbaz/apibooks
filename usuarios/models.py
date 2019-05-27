# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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


class LibrosSeguidos(models.Model):
    usuario = models.ForeignKey('Usuarios', on_delete=models.CASCADE)
    libro = models.ForeignKey('libros.Libros', on_delete=models.CASCADE)
    ultimo_capitulo = models.IntegerField(blank=False, null=False)
    ultima_visita = models.DateTimeField(default=timezone.now)


    def __unicode__(self):
        return "Usuario {0} sigue {1}".format(self.usuario.usuario.username, self.libro.titulo)

    class Meta:
        unique_together = ('usuario', 'libro',)
        verbose_name = 'Libros seguidos'
        verbose_name_plural = 'Libros seguidos'
