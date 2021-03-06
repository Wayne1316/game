# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-02 12:50
from __future__ import unicode_literals

import core.helper
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='start')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='end')),
                ('status', models.CharField(choices=[('calc', 'status calc'), ('close', 'status close'), ('edit', 'status edit'), ('open', 'status open')], default='edit', max_length=30, verbose_name='table status')),
                ('form', models.CharField(choices=[('national_read', 'national read game'), ('no_game', 'no game'), ('normal', 'normal game'), ('read', 'read game'), ('thesis', 'thesis game')], default='no_game', max_length=30, verbose_name='table form')),
                ('title', models.CharField(max_length=255, verbose_name='activity title')),
                ('year', models.CharField(max_length=100, null=True, verbose_name='activity year')),
                ('term', models.CharField(max_length=100, null=True, verbose_name='activity term')),
                ('descript', models.TextField(blank=True, null=True, verbose_name='activity descript')),
                ('exam_notice', models.TextField(blank=True, null=True, verbose_name='activity exam notice')),
                ('exam_descript', models.CharField(max_length=100, null=True, verbose_name='activity exam description')),
                ('result_descript', models.TextField(blank=True, null=True, verbose_name='activity result description')),
                ('is_copy', models.BooleanField(default=False, verbose_name='oeen copy')),
                ('is_suggest', models.BooleanField(default=False, verbose_name='open suggest')),
                ('is_lock', models.BooleanField(default=False, verbose_name='open lock')),
                ('is_show_form', models.BooleanField(default=False, verbose_name='open form')),
                ('is_game', models.BooleanField(default=True, verbose_name='table is_game')),
            ],
            options={
                'verbose_name': 'table activity',
                'verbose_name_plural': 'table activity',
            },
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=100, verbose_name='award title')),
            ],
            options={
                'verbose_name': 'table award',
                'verbose_name_plural': 'table award',
            },
        ),
        migrations.CreateModel(
            name='AwardSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('priority', models.IntegerField(verbose_name='priority')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Activity', verbose_name='table activity')),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Award', verbose_name='table award')),
            ],
            options={
                'verbose_name': 'table award setting',
                'verbose_name_plural': 'table award setting',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=45, verbose_name='group title')),
            ],
            options={
                'verbose_name': 'table group',
                'verbose_name_plural': 'table group',
            },
        ),
        migrations.CreateModel(
            name='GroupSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('priority', models.IntegerField(verbose_name='priority')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Activity', verbose_name='table activity')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Group', verbose_name='table group')),
                ('jury', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='table jury')),
            ],
            options={
                'verbose_name': 'table group setting',
                'verbose_name_plural': 'table group setting',
                'permissions': (('review', 'review permission'),),
            },
        ),
        migrations.CreateModel(
            name='Jury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Activity', verbose_name='table activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'table jury',
                'verbose_name_plural': 'table jury',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='member name')),
                ('member_class', models.CharField(blank=True, max_length=100, null=True, verbose_name='member class')),
                ('setno', models.CharField(blank=True, max_length=100, null=True, verbose_name='member set number')),
            ],
            options={
                'verbose_name': 'table member',
                'verbose_name_plural': 'table member',
            },
        ),
        migrations.CreateModel(
            name='MemberType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='member type')),
            ],
            options={
                'verbose_name': 'table member type',
                'verbose_name_plural': 'table member type',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('score', models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True, verbose_name='score')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='comment')),
                ('is_copy', models.BooleanField(default=False, verbose_name='copy')),
                ('is_suggest', models.BooleanField(default=False, verbose_name='suggest')),
                ('jury', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='table jury')),
            ],
            options={
                'verbose_name': 'table review',
                'verbose_name_plural': 'table review',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='subject title')),
                ('banner', models.ImageField(blank=True, null=True, upload_to=core.helper.RandomFileName('subject/'), verbose_name='subject banner')),
            ],
            options={
                'verbose_name': 'table subject',
                'verbose_name_plural': 'table subject',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='work name')),
                ('team_title', models.CharField(max_length=255, verbose_name='team name')),
                ('file', models.FileField(blank=True, null=True, upload_to=core.helper.RandomFileName('game/'), verbose_name='team file')),
                ('book_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='book title')),
                ('author', models.CharField(blank=True, max_length=255, null=True, verbose_name='author')),
                ('isbn', models.CharField(blank=True, max_length=255, null=True, verbose_name='ISBN')),
                ('publish_date', models.CharField(blank=True, max_length=255, null=True, verbose_name='publish date')),
                ('version', models.CharField(blank=True, max_length=255, null=True, verbose_name='version')),
                ('publisher', models.CharField(blank=True, max_length=255, null=True, verbose_name='publisher')),
                ('page', models.CharField(blank=True, max_length=255, null=True, verbose_name='page')),
                ('abstract', models.TextField(blank=True, null=True, verbose_name='abstract')),
                ('extract', models.TextField(blank=True, null=True, verbose_name='extract')),
                ('opinion', models.TextField(blank=True, null=True, verbose_name='opinion')),
                ('discuss', models.TextField(blank=True, null=True, verbose_name='discuss')),
                ('is_copy', models.BooleanField(default=False, verbose_name='copy')),
                ('is_suggest', models.BooleanField(default=False, verbose_name='suggest')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('award', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.AwardSetting', verbose_name='table award setting')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.GroupSetting', verbose_name='table group setting')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'table team',
                'verbose_name_plural': 'table team',
            },
        ),
        migrations.AddField(
            model_name='review',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Team', verbose_name='table team'),
        ),
        migrations.AddField(
            model_name='member',
            name='member_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.MemberType', verbose_name='table member type'),
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Team', verbose_name='table team'),
        ),
        migrations.AddField(
            model_name='activity',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Subject', verbose_name='table subject'),
        ),
        migrations.CreateModel(
            name='NationalReadActivity',
            fields=[
            ],
            options={
                'verbose_name': 'national read game',
                'proxy': True,
                'verbose_name_plural': 'national read game',
                'indexes': [],
            },
            bases=('game.activity',),
        ),
        migrations.CreateModel(
            name='NoGameActivity',
            fields=[
            ],
            options={
                'verbose_name': 'no game',
                'proxy': True,
                'verbose_name_plural': 'no game',
                'indexes': [],
            },
            bases=('game.activity',),
        ),
        migrations.CreateModel(
            name='NormalActivity',
            fields=[
            ],
            options={
                'verbose_name': 'normal game',
                'proxy': True,
                'verbose_name_plural': 'normal game',
                'indexes': [],
            },
            bases=('game.activity',),
        ),
        migrations.CreateModel(
            name='ReadActivity',
            fields=[
            ],
            options={
                'verbose_name': 'read game',
                'proxy': True,
                'verbose_name_plural': 'read game',
                'indexes': [],
            },
            bases=('game.activity',),
        ),
        migrations.CreateModel(
            name='ThesisActivity',
            fields=[
            ],
            options={
                'verbose_name': 'thesis game',
                'proxy': True,
                'verbose_name_plural': 'thesis game',
                'indexes': [],
            },
            bases=('game.activity',),
        ),
    ]
