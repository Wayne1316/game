# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from .models import Activity, GroupSetting


def activity_is_join(pk):
    res = Activity.objects.join().filter(pk=pk)
    if res.count() == 1 and res[0].form != 'no_game':
        return True
    raise ObjectDoesNotExist


def group_is_jury(pk, user):
    res = GroupSetting.objects.jury(user, pk=pk)
    if res.count() == 1:
        return True
    raise PermissionDenied
