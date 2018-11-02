# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from suit_redactor.widgets import RedactorWidget


class PosterForm(forms.ModelForm):
    class Meta:
        widgets = {
            'html': RedactorWidget(editor_options={'startupFocus': True, 'width': 640, 'height': 400}),
        }
