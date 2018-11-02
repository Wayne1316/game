# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps

from .helper import activity_is_join, group_is_jury


def join_required(view_func):
    @wraps(view_func)
    def check(request, *args, **kwargs):
        activity_is_join(kwargs['pk'])
        response = view_func(request, *args, **kwargs)
        return response
    return check


def has_jury_data(view_func):
    @wraps(view_func)
    def check(request, *args, **kwargs):
        group_is_jury(kwargs['pk'], request.user)
        response = view_func(request, *args, **kwargs)
        return response
    return check
