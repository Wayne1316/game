# -*- coding: utf-8 -*-
from django import template

from users.form import LoginForm


register = template.Library()


@register.assignment_tag
def get_login_form():
    return LoginForm

