# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

from .import manager


class Visit(TimeStampedModel):
    quantity = models.IntegerField(_("visit"),)
    objects = manager.VisitManager()
