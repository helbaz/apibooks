# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Usuarios(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Comentarios(models.Model):
    usuario = models.ForeignKey(Usuarios)
    comentario = models.CharField(max_length=500)
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'