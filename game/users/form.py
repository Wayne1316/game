# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField, CaptchaTextInput

from core import kmsh
from core.logger import auth_logger
from core.widgets import UKTextInput


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=UKTextInput(attrs={'placeholder': _('please input username')}))
    password = forms.CharField(widget=UKTextInput(
        attrs={
            'placeholder': _('please input password'),
            'type': 'password',
        }
    ))
    if not settings.SKIP_CAPTCHA:
        captcha = CaptchaField(widget=CaptchaTextInput(field_template='captcha/widgets/login.html'))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.error_messages['invalid_username'] = _('username not exists')
        self.error_messages['account_expired'] = _('account has expired')
        self.error_messages['unknown_exception'] = _('unknown exception:\n error message %(error_message)s')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.authenticate_outer(username, password)
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def authenticate_outer(self, username, password):
        try:
            auth_logger().info('user <{username}> login'.format(username=username))
            kmsh.authenticate(username, password)
        except kmsh.UserNotExistsException as e:
            auth_logger().exception(e.message, exc_info=True)
            raise forms.ValidationError(
                self.error_messages['invalid_username'],
                code='invalid_login',
            )
        except kmsh.PasswordInvaildException as e:
            auth_logger().exception(e.message, exc_info=True)
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )
        except kmsh.AccountExpiredException as e:
            auth_logger().exception(e.message, exc_info=True)
            raise forms.ValidationError(
                self.error_messages['account_expired'],
                code='invalid_login',
            )
        except Exception as e:
            auth_logger().error(e.message, exc_info=True)
            raise forms.ValidationError(
                self.error_messages['unknown_exception'],
                code='invalid_login',
                params={'error_message': e.message},
            )

    def as_div(self):
        return self._html_output(
            normal_row='<div class="uk-form-row">%(field)s%(help_text)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)


