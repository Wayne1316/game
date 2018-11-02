# -*- coding: utf-8 -*-
from django.db.models import Q
from django.contrib.auth.models import Permission


def user_with_perm(codename):
    perm = Permission.objects.get(codename=codename)
    return Q(is_superuser=True) | Q(user_permissions=perm) | Q(groups__permissions=perm)
