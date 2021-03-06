# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-19 01:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='poster title')),
                ('html', models.TextField(blank=True, null=True, verbose_name='html')),
            ],
            options={
                'verbose_name': 'table poster',
                'verbose_name_plural': 'table poster',
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='style title')),
            ],
            options={
                'verbose_name': 'table style',
                'verbose_name_plural': 'table style',
            },
        ),
        migrations.AddField(
            model_name='poster',
            name='style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poster.Style', verbose_name='table style'),
        ),
    ]
