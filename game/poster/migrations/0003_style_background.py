# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-26 07:21
from __future__ import unicode_literals

import core.helper
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0002_style_orientation'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='background',
            field=models.ImageField(default='', upload_to=core.helper.RandomFileName('poster/'), verbose_name='style background'),
            preserve_default=False,
        ),
    ]