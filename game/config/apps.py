# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem
from poster.apps import PosterConfig
from game.apps import GameConfig
from django.contrib.auth.apps import AuthConfig


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
    menu = [
        ParentItem(AuthConfig.verbose_name, children=[
            ChildItem(model='auth.user'),
            ChildItem(model='auth.group'),
        ], icon='fa fa-users'),
    ]
    menu = PosterConfig.menu + GameConfig.menu + menu
