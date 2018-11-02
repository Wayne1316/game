# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

from . import models


register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name


@register.inclusion_tag('components/error_list.html', takes_context=True)
def error_list(context, errors):
    return {
        'errors': errors
    }


@register.simple_tag
def id_name(name):
    return mark_safe('id="{id}" name="{name}"'.format(id=name, name=name))


@register.simple_tag
def if_string(condition, string):
    if condition:
        return mark_safe(string)
    else:
        return ''


@register.simple_tag
def checked(condition):
    return if_string(condition, 'checked')


@register.simple_tag
def visit_quantity():
    return models.Visit.objects.newest().quantity


@register.filter
def index(array, i):
    try:
        return array[int(i)-1]
    except IndexError:
        pass
    return None

