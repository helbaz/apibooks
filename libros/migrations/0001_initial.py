# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-13 17:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import libros.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capitulos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('num_capitulo', models.IntegerField()),
                ('contenido', models.CharField(max_length=100)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Capitulo',
                'verbose_name_plural': 'Capitulos',
            },
        ),
        migrations.CreateModel(
            name='Generos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Genero',
                'verbose_name_plural': 'Generos',
            },
        ),
        migrations.CreateModel(
            name='Libros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('imagen_perfil', models.ImageField(blank=True, default='static/default_book.png', null=True, upload_to=libros.models.get_image_path)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Usuarios')),
                ('generos', models.ManyToManyField(blank=True, to='libros.Generos')),
            ],
            options={
                'verbose_name': 'Libro',
                'verbose_name_plural': 'Libros',
            },
        ),
        migrations.AddField(
            model_name='capitulos',
            name='libro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libros.Libros'),
        ),
    ]
