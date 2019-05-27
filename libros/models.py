# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from usuarios.models import *

# Create your models here.
def get_image_path(instance, filename):
    id = 0
    if instance.id is None:
        id = 'temp'
        print id
    else:
        id = instance.id
    return os.path.join('static/books/', str(id), filename)


class Generos(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'

    def __unicode__(self):
        return self.nombre


class Libros(models.Model):
    titulo = models.CharField(max_length=100, blank=False, null=False, unique=True)
    descripcion = models.CharField(max_length=500, blank=False, null=False)
    generos = models.ManyToManyField(Generos, blank=True)
    autor = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    imagen_perfil = models.ImageField(upload_to=get_image_path, blank=True, null=True, default='static'
                                                                                               '/default_book.png')

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __unicode__(self):
        return self.titulo


class Capitulos(models.Model):
    titulo = models.CharField(max_length=100, blank=False, null=False)
    num_capitulo = models.IntegerField(blank=False, null=False)
    contenido = models.TextField(blank=False, null=False)
    libro = models.ForeignKey(Libros, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('num_capitulo', 'libro',)
        verbose_name = 'Capitulo'
        verbose_name_plural = 'Capitulos'

    def __unicode__(self):
        return "Capítulo {0}: {1} - {2}".format(str(self.num_capitulo), self.titulo, self.libro.titulo)
