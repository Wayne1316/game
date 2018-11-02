# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib import admin as admin_site
from django.utils.translation import ugettext_lazy as _


admin_site.site.site_title = _('game administration')
admin_site.site.site_header = _('game administration')
admin_site.site.index_title = _('KMSH library game administration')
admin_site.site.site_url = settings.FORCE_SCRIPT_NAME if settings.FORCE_SCRIPT_NAME else '/'
