# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-12 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0007_petition_overview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='overview',
            field=models.TextField(help_text='A brief overview of petition subject encouraging the signing of the petition.', verbose_name='Overview'),
        ),
    ]
