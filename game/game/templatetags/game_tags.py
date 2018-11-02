# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text


from game.models import (
    Subject,
    Activity
)


register = template.Library()


@register.assignment_tag
def get_subjects():
    return Subject.objects.all()


@register.filter
@stringfilter
def form_value(text):
    name = force_text(text)
    return getattr(Activity.FORM, name).value[1]


@register.filter
@stringfilter
def status_value(text):
    name = force_text(text)
    return getattr(Activity.STATUS, name).value[1]


@register.inclusion_tag('game/join_field.html', takes_context=True)
def join_field(context, field_name, field):
    return {
        'field_name': field_name,
        'field': field
    }
