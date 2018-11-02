# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _


from . import models


class ReviewValidMixin(object):
    @staticmethod
    def team_valid(data):
        if not models.Team.objects.calc(pk=data.get('team').pk):
            forms.ValidationError(_('status not in review'))

    @staticmethod
    def permission_valid(data):
        user = data.get('jury', None)
        if user is None:
            forms.ValidationError(_('user not found'))
        if not user.has_perm('game.review') and len(models.Team.objects.review(user)) != 1:
            forms.ValidationError(_("you don't have permission to review"))

    @staticmethod
    def copy_valid(data):
        if data.get('is_copy', None) is not None and \
                not models.Team.objects.filter(pk=data.get('team').pk).first().group.activity.is_copy:
            forms.ValidationError(_("you don't have permission to edit this field"))

    @staticmethod
    def suggest_valid(data):
        if data.get('is_suggest', None) is not None and \
                not models.Team.objects.filter(pk=data.get('team').pk).first().group.activity.is_suggest:
            forms.ValidationError(_("you don't have permission to edit this field"))

    def valid_extra(self, data):
        self.team_valid(data)
        self.permission_valid(data)
        self.copy_valid(data)
        self.suggest_valid(data)


class ReviewSaveMixin(object):
    def save(self):
        defaults = {
            'score': self.cleaned_data['score'],
            'comment': self.cleaned_data['comment'],
        }
        if self.cleaned_data['is_copy'] is not None:
            defaults['is_copy'] = self.cleaned_data['is_copy']
        if self.cleaned_data['is_suggest'] is not None:
            defaults['is_suggest'] = self.cleaned_data['is_suggest']

        return models.Review.objects.update_or_create(
            team_id=self.cleaned_data['team'].pk,
            jury_id=self.cleaned_data['jury'].pk,
            defaults=defaults
        )
