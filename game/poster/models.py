# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from enum import Enum
from model_utils.models import TimeStampedModel

from core.helper import RandomFileName


@python_2_unicode_compatible
class Style(TimeStampedModel):
    class Orientation(Enum):
        portrait = ('portrait', _('portrait'))
        landscape = ('landscape', _('landscape'))
    title = models.CharField(_("style title"), max_length=255)
    background = models.ImageField(_("style background"), upload_to=RandomFileName('poster/'))
    orientation = models.CharField(
        verbose_name=_("orientation"),
        choices=[x.value for x in Orientation],
        max_length=10,
        default=getattr(Orientation.portrait, 'value')[0],
    )

    class Meta:
        verbose_name = _("table style")
        verbose_name_plural =_("table style")

    def __str__(self):
        return "{title}/{orientation}".format(
            title=self.title,
            orientation=getattr(self.Orientation, self.orientation).value[1],
        )


@python_2_unicode_compatible
class Poster(TimeStampedModel):
    style = models.ForeignKey(Style, verbose_name=_("table style"))
    title = models.CharField(_("poster title"), max_length=255)
    html = models.TextField(_("html"), null=True, blank=True)

    class Meta:
        verbose_name = _("table poster")
        verbose_name_plural =_("table poster")

    def __str__(self):
        return self.title


class Temp(models.Model):
    file = models.FileField(upload_to=RandomFileName('poster/'))
