# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-03 07:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='exam_notice',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='is_game',
        ),
    ]