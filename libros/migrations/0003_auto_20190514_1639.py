# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-14 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import libros.models


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0002_auto_20190514_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libros',
            name='imagen_perfil',
            field=models.ImageField(blank=True, default='static/default_book.png', null=True, upload_to=libros.models.get_image_path),
        ),
    ]
