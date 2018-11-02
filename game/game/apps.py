# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from suit.menu import ParentItem, ChildItem


class GameConfig(AppConfig):
    name = 'game'
    verbose_name = _('game')

    menu = [
        ParentItem(verbose_name, children=[
            ChildItem(model='game.nogameactivity'),
            ChildItem(model='game.normalactivity'),
            ChildItem(model='game.thesisactivity'),
            ChildItem(model='game.nationalreadactivity'),
            ChildItem(model='game.readactivity'),
        ], icon='fa fa-leaf'),
        ParentItem(_('parameter setting'), children=[
            ChildItem(model='game.subject'),
            ChildItem(model='game.award'),
            ChildItem(model='game.group'),
            ChildItem(model='game.membertype'),
        ], icon='fa fa-leaf'),
    ]
