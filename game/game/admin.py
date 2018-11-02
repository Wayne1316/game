# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from core.fields import model_edit_fields
from game.admin_base import BaseActivityAdmin
from .models import (
    Award,
    Group,
    MemberType,
    Subject,
    NoGameActivity,
    NormalActivity,
    ThesisActivity,
    NationalReadActivity,
    ReadActivity,
    GroupSetting,
    AwardSetting,
    Team,
    Member,
    Review,
)


class MemberInline(admin.TabularInline):
    model = Member
    extra = 1
    suit_classes = 'suit-tab suit-tab-member'


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    suit_classes = 'suit-tab suit-tab-review'


class TeamAdmin(admin.ModelAdmin):
    list_display = ('title', )
    inlines = (MemberInline, ReviewInline,)

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': model_edit_fields(Team)
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-member',),
            'fields': ()
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-review',),
            'fields': ()
        }),
    )

    suit_form_tabs = (
        ('general', _('activity information')),
        ('member', _('table member')),
        ('review', _('table review')),
    )


class NoGameAdmin(BaseActivityAdmin):
    fieldsets = tuple()
    suit_form_tabs = tuple()
    inlines = tuple()
    fields = ('subject', 'title', 'year', 'term', 'status', 'descript', 'result_descript', 'start', 'end')


admin.site.register(Award)
admin.site.register(Group)
admin.site.register(MemberType)
admin.site.register(Subject)
admin.site.register(GroupSetting)
admin.site.register(NoGameActivity, NoGameAdmin)
admin.site.register(NormalActivity, BaseActivityAdmin)
admin.site.register(ThesisActivity, BaseActivityAdmin)
admin.site.register(NationalReadActivity, BaseActivityAdmin)
admin.site.register(ReadActivity, BaseActivityAdmin)
admin.site.register(AwardSetting)
admin.site.register(Team, TeamAdmin)
admin.site.register(Member)
admin.site.register(Review)
