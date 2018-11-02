# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from suit.menu import ParentItem, ChildItem


class PosterConfig(AppConfig):
    name = 'poster'
    verbose_name = _('poster')
    menu = [
        ParentItem(verbose_name, children=[
            ChildItem(model='poster.style'),
            ChildItem(model='poster.poster'),
        ], icon='fa fa-leaf'),
    ]
