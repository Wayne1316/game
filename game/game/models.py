# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from enum import Enum
from model_utils.models import TimeStampedModel, TimeFramedModel

from core.helper import RandomFileName
from .manager import (
    ActivityManager,
    TeamManager,
    GroupSettingManager
)


@python_2_unicode_compatible
class Award(TimeStampedModel):
    title = models.CharField(_("award title"), max_length=100)

    class Meta:
        verbose_name = _("table award")
        verbose_name_plural = _("table award")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Group(TimeStampedModel):
    title = models.CharField(_("group title"), max_length=45)

    class Meta:
        verbose_name = _("table group")
        verbose_name_plural = _("table group")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Subject(TimeStampedModel):
    title = models.CharField(_("subject title"), max_length=255)
    banner = models.ImageField(_("subject banner"), upload_to=RandomFileName('subject/'), null=True, blank=True)

    class Meta:
        verbose_name = _("table subject")
        verbose_name_plural = _("table subject")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class MemberType(TimeStampedModel):
    title = models.CharField(_("member type"), max_length=255)

    class Meta:
        verbose_name = _("table member type")
        verbose_name_plural = _("table member type")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Activity(TimeStampedModel, TimeFramedModel):
    class STATUS(Enum):
        edit = ('edit', _('status edit'))
        open = ('open', _('status open'))
        calc = ('calc', _('status calc'))
        close = ('close', _('status close'))

    class FORM(Enum):
        no_game = ('no_game', _('no game'))
        normal = ('normal', _('normal game'))
        thesis = ('thesis', _('thesis game'))
        national_read = ('national_read', _('national read game'))
        read = ('read', _('read game'))

    status = models.CharField(
        verbose_name=_("table status"),
        choices=[x.value for x in STATUS],
        max_length=30,
        default=getattr(STATUS.edit, 'value')[0],
    )
    form = models.CharField(
        verbose_name=_("table form"),
        choices=[x.value for x in FORM],
        max_length=30,
        default=getattr(FORM.no_game, 'value')[0],
    )
    subject = models.ForeignKey(Subject, verbose_name=_("table subject"))
    title = models.CharField(_("activity title"), max_length=255)
    year = models.CharField(_("activity year"), max_length=100, null=True)
    term = models.CharField(_("activity term"), max_length=100, null=True)
    descript = models.TextField(_("activity descript"), blank=True, null=True)
    exam_descript = models.CharField(_("activity exam description"), max_length=100, null=True)
    result_descript = models.TextField(_("activity result description"), blank=True, null=True)
    is_copy = models.BooleanField(_("oeen copy"), default=False)
    is_suggest = models.BooleanField(_("open suggest"), default=False)
    is_lock = models.BooleanField(_("open lock"), default=False)
    is_show_form = models.BooleanField(_("open form"), default=False)

    objects = ActivityManager()

    class Meta:
        verbose_name = _("table activity")
        verbose_name_plural = _("table activity")

    def __str__(self):
        return self.title


class NoGameActivity(Activity):
    objects = ActivityManager(default_form=getattr(Activity.FORM.no_game, 'name'))

    class Meta:
        proxy = True
        verbose_name = _('no game')
        verbose_name_plural = _('no game')

    def save(self, *args, **kwargs):
        if self.form is not None:
            self.form = getattr(Activity.FORM.no_game, 'name')
        super(NoGameActivity, self).save(*args, **kwargs)


class NormalActivity(Activity):
    objects = ActivityManager(default_form=getattr(Activity.FORM.normal, 'name'))

    class Meta:
        proxy = True
        verbose_name = _('normal game')
        verbose_name_plural = _('normal game')

    def save(self, *args, **kwargs):
        if self.form is not None:
            self.form = getattr(Activity.FORM.normal, 'name')
        super(NormalActivity, self).save(*args, **kwargs)


class ThesisActivity(Activity):
    objects = ActivityManager(default_form=getattr(Activity.FORM.thesis, 'name'))

    class Meta:
        proxy = True
        verbose_name = _('thesis game')
        verbose_name_plural = _('thesis game')

    def save(self, *args, **kwargs):
        if self.form is not None:
            self.form = getattr(Activity.FORM.thesis, 'name')
        super(ThesisActivity, self).save(*args, **kwargs)


class NationalReadActivity(Activity):
    objects = ActivityManager(default_form=getattr(Activity.FORM.national_read, 'name'))

    class Meta:
        proxy = True
        verbose_name = _('national read game')
        verbose_name_plural = _('national read game')

    def save(self, *args, **kwargs):
        if self.form is not None:
            self.form = getattr(Activity.FORM.national_read, 'name')
        super(NationalReadActivity, self).save(*args, **kwargs)


class ReadActivity(Activity):
    objects = ActivityManager(default_form=getattr(Activity.FORM.read, 'name'))

    class Meta:
        proxy = True
        verbose_name = _('read game')
        verbose_name_plural = _('read game')

    def save(self, *args, **kwargs):
        if self.form is not None:
            self.form = getattr(Activity.FORM.read, 'name')
        super(ReadActivity, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Jury(TimeStampedModel):
    activity = models.ForeignKey(Activity, verbose_name=_("table activity"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))

    class Meta:
        verbose_name = _("table jury")
        verbose_name_plural = _("table jury")

    def __str__(self):
        return self.user.username


@python_2_unicode_compatible
class GroupSetting(TimeStampedModel):
    activity = models.ForeignKey(Activity, verbose_name=_("table activity"))
    group = models.ForeignKey(Group, verbose_name=_("table group"))
    priority = models.IntegerField(_("priority"))
    jury = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("table jury"))

    objects = GroupSettingManager()

    class Meta:
        verbose_name = _("table group setting")
        verbose_name_plural = _("table group setting")
        permissions = (('review', _('review permission'),),)

    def __str__(self):
        return "{activity} {group}".format(
            activity=self.activity.title,
            group=self.group.title,
        )


@python_2_unicode_compatible
class AwardSetting(TimeStampedModel):
    activity = models.ForeignKey(Activity, verbose_name=_("table activity"))
    award = models.ForeignKey(Award, verbose_name=_("table award"))
    priority = models.IntegerField(_("priority"))

    class Meta:
        verbose_name = _("table award setting")
        verbose_name_plural = _("table award setting")

    def __str__(self):
        return self.award.title


@python_2_unicode_compatible
class Team(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("owner"))
    group = models.ForeignKey(GroupSetting, verbose_name=_("table group setting"))
    award = models.ForeignKey(AwardSetting, verbose_name=_("table award setting"), null=True)

    title = models.CharField(_("work name"), max_length=255)
    team_title = models.CharField(_("team name"), max_length=255)
    file = models.FileField(_("team file"), upload_to=RandomFileName('game/'), null=True, blank=True)
    book_title = models.CharField(_("book title"), max_length=255, null=True, blank=True)
    author = models.CharField(_("author"), max_length=255, null=True, blank=True)
    isbn = models.CharField(_("ISBN"), max_length=255, null=True, blank=True)
    publish_date = models.CharField(_("publish date"), max_length=255, null=True, blank=True)
    version = models.CharField(_("version"), max_length=255, null=True, blank=True)
    publisher = models.CharField(_("publisher"), max_length=255, null=True, blank=True)
    page = models.CharField(_("page"), max_length=255, null=True, blank=True)
    abstract = models.TextField(_("abstract"), null=True, blank=True)
    extract = models.TextField(_("extract"), null=True, blank=True)
    opinion = models.TextField(_("opinion"), null=True, blank=True)
    discuss = models.TextField(_("discuss"), null=True, blank=True)
    is_copy = models.BooleanField(_("copy"), default=False)
    is_suggest = models.BooleanField(_("suggest"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    objects = TeamManager()

    class Meta:
        verbose_name = _("table team")
        verbose_name_plural = _("table team")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Member(TimeStampedModel):
    team = models.ForeignKey(Team, verbose_name=_("table team"))
    member_type = models.ForeignKey(MemberType, verbose_name=_("table member type"))

    name = models.CharField(_("member name"), max_length=100)
    member_class = models.CharField(_("member class"), max_length=100, null=True, blank=True)
    setno = models.CharField(_("member set number"), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("table member")
        verbose_name_plural = _("table member")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Review(TimeStampedModel):
    team = models.ForeignKey(Team, verbose_name=_("table team"))
    jury = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("table jury"))

    score = models.DecimalField(_('score'), max_digits=5, decimal_places=2, null=True, default=0)
    comment = models.TextField(_('comment'), null=True, blank=True)
    is_copy = models.BooleanField(_("copy"), default=False)
    is_suggest = models.BooleanField(_("suggest"), default=False)

    class Meta:
        verbose_name = _("table review")
        verbose_name_plural = _("table review")

    def __str__(self):
        return '{jury} <{comment}>'.format(
            jury=self.jury.username,
            comment=self.comment,
        )
