# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-21 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0005_auto_20190520_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitulos',
            name='libro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libros.Libros', unique=True),
        ),
        migrations.AlterField(
            model_name='capitulos',
            name='num_capitulo',
            field=models.IntegerField(unique=True),
        ),
    ]
