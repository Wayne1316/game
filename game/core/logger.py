# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging


def dev_logger():
    return logging.getLogger('dev')


def auth_logger():
    return logging.getLogger('auth')
