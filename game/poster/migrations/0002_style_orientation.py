# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-26 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='orientation',
            field=models.CharField(choices=[('landscape', 'landscape'), ('portrait', 'landscape')], default='portrait', max_length=10, verbose_name='orientation'),
        ),
    ]
