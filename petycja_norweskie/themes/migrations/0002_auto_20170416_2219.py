# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-16 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='prefix',
            field=models.CharField(max_length=25, unique=True, verbose_name='System name of theme prefix'),
        ),
    ]
