# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-23 15:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0008_auto_20190521_1341'),
        ('usuarios', '0004_auto_20190523_1504'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='librosseguidos',
            unique_together=set([('usuario', 'libro')]),
        ),
    ]