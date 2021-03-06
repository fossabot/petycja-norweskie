# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-09 23:43
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models

import petycja_norweskie.menu.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                                      verbose_name='modified')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('url', models.CharField(max_length=100,
                                         validators=[petycja_norweskie.menu.validators.is_external_or_valid_url],
                                         verbose_name='URL')),
                ('visible', models.BooleanField(default=False, help_text='Check to mark element as public visible',
                                                verbose_name='Public visible')),
                ('position', models.SmallIntegerField(default=0, verbose_name='Position')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                             to='menu.Element', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Element',
                'ordering': ['position'],
                'verbose_name_plural': 'Elements',
            },
        ),
    ]
