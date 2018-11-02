# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid

from django.utils.deconstruct import deconstructible
from django.conf import settings


@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)


def get_site_uri(request):
    if getattr(settings, 'SITE_URI', None):
        return settings.SITE_URI
    else:
        return "{protocol}://{host}".format(
            protocol=request.META['wsgi.url_scheme'],
            host=request.META['HTTP_HOST'],
        )
