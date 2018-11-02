# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from . import models


class ProfileInline(admin.StackedInline):
    model = models.Profile
    extra = 1
    min_num = 1
    verbose_name_plural = _('other information')


class UserMailInline(admin.TabularInline):
    model = models.UserMail
    extra = 1
    verbose_name_plural = _('email')


class OverrideUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    inlines = (ProfileInline, UserMailInline, )


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), OverrideUserAdmin)
