# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel):
    uid = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(_('phone'), max_length=100)


class UserMail(TimeStampedModel):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL)
    email = models.CharField(_('email'), max_length=255, blank=True, null=True)
