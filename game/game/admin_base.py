# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from core.fields import model_edit_fields
from .form import (
    GroupSettingFrom,
    ActivityForm,
)
from .models import (
    AwardSetting,
    GroupSetting,
    Activity,
)


class GroupSettingInline(admin.TabularInline):
    model = GroupSetting
    fields = ('group', 'priority', 'jury', 'link_to_team')
    readonly_fields = ('link_to_team', )
    extra = 1
    suit_classes = 'suit-tab suit-tab-groupsetting'
    form = GroupSettingFrom

    @staticmethod
    def link_to_team(obj):
        if obj.id is not None:
            return format_html(
                '<a class="button" href="{}?group__id__exact={}">{}</a',
                reverse('admin:game_team_changelist'),
                obj.id,
                _('table team'),
            )
        return ''


class AwardSettingInline(admin.TabularInline):
    model = AwardSetting
    extra = 1
    suit_classes = 'suit-tab suit-tab-awardsetting'


class BaseActivityAdmin(admin.ModelAdmin):
    inlines = (AwardSettingInline, GroupSettingInline, )
    exclude = ['form']
    form = ActivityForm
    result_field = ['result_descript']
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': model_edit_fields(Activity, exclude + result_field)
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-awardsetting',),
            'fields': ()
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-groupsetting',),
            'fields': ()
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-resultsetting',),
            'fields': result_field
        }),
    )

    suit_form_tabs = (
        ('general', _('activity information')),
        ('awardsetting', _('table award setting')),
        ('groupsetting', _('table group setting')),
        ('resultsetting', _('table result setting')),
    )

