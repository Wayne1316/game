# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.views import LoginView

from .form import LoginForm


class Login(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
