# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class UKTextInput(forms.TextInput):
    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        else:
            attrs = {}
        attrs['class'] = 'uk-form-large uk-width-responsive'
        super(UKTextInput, self).__init__(attrs)

