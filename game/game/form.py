# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from suit_redactor.widgets import RedactorWidget

from core.permission import user_with_perm
from .models import MemberType, GroupSetting, Team
from .form_mixins import ReviewValidMixin, ReviewSaveMixin


class GroupSettingFrom(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupSettingFrom, self).__init__(*args, **kwargs)
        self.fields['jury'].queryset = get_user_model().objects.filter(user_with_perm('review'))
        self.fields['jury'].empty_label = None


class ActivityForm(forms.ModelForm):
    class Meta:
        widgets = {
            'descript': RedactorWidget(editor_options={'startupFocus': True, 'width': 640, 'height': 400}),
            'exam_notice': RedactorWidget(editor_options={'startupFocus': True, 'width': 640, 'height': 400}),
            'result_descript': RedactorWidget(editor_options={'startupFocus': True, 'width': 640, 'height': 400}),
        }


class TeacherFrom(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    member_type = forms.ModelChoiceField(queryset=MemberType.objects.get_queryset())


class MemberForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    member_class = forms.CharField(max_length=100, required=True)
    setno = forms.CharField(max_length=100, required=True)
    member_type = forms.ModelChoiceField(queryset=MemberType.objects.get_queryset())


class JoinBaseForm(forms.Form):
    group = forms.IntegerField(required=True)
    title = forms.CharField(max_length=255, required=True)

    def clean(self, *args, **kwargs):
        cleaned_data = super(JoinBaseForm, self).clean(*args, **kwargs)
        group = cleaned_data.get('group', None)
        if group and GroupSetting.objects.filter(pk=group).count() == 0:
            raise forms.ValidationError(_('group not exists!!'))
        cleaned_data['group'] = GroupSetting.objects.get(pk=group)
        return cleaned_data


class ReadForm(JoinBaseForm):
    book_title = forms.CharField(max_length=255, required=True)
    author = forms.CharField(max_length=255, required=True)
    isbn = forms.CharField(max_length=255, required=False, initial='')
    publish_date = forms.CharField(max_length=255, required=False, initial='')
    version = forms.CharField(max_length=255, required=False, initial='')
    publisher = forms.CharField(max_length=255, required=False, initial='')
    page = forms.CharField(max_length=255, required=False, initial='')
    file = forms.FileField(required=True)


class NationalReadForm(JoinBaseForm):
    book_title = forms.CharField(max_length=255, required=True)
    author = forms.CharField(max_length=255, required=True)
    isbn = forms.CharField(max_length=255, required=False, initial='')
    publish_date = forms.CharField(max_length=255, required=False, initial='')
    version = forms.CharField(max_length=255, required=False, initial='')
    publisher = forms.CharField(max_length=255, required=False, initial='')
    page = forms.CharField(max_length=255, required=False, initial='')
    abstract = forms.CharField(max_length=250, min_length=100, required=True)
    extract = forms.CharField(max_length=350, required=True)
    opinion = forms.CharField(max_length=1000, required=True)
    discuss = forms.CharField(required=True)


class NormalForm(JoinBaseForm):
    file = forms.FileField(required=True)


class ThesisForm(JoinBaseForm):
    file = forms.FileField(required=True)


class JoinForm(object):
    member_size = 2
    member_field = ('member_class', 'name', 'setno')

    def __init__(self, activity, data, files):
        self.activity = activity
        self.member_forms = []
        self.teacher_forms = []

        if self.activity.form == 'read':
            self.form = ReadForm(data, files)
        elif self.activity.form == 'national_read':
            self.form = NationalReadForm(data, files)
        elif self.activity.form == 'normal':
            self.form = NormalForm(data, files)
        elif self.activity.form == 'thesis':
            self.form = ThesisForm(data, files)
            members = self.prepare_members(data)
            for member in members:
                if any([field[1] for field in member.items()]):
                    member.update({'member_type': 2})
                    self.member_forms.append(MemberForm(member))
        for teacher in data.getlist('teacher'):
            if teacher:
                self.teacher_forms.append(TeacherFrom(data={'name': teacher, 'member_type': 1}))

    def is_valid(self):
        is_pass = True
        if not self.form.is_valid():
            is_pass = False
        for form in self.teacher_forms:
            if not form.is_valid():
                is_pass = False
        for form in self.member_forms:
            if not form.is_valid():
                is_pass = False
        return is_pass

    def cleaned_data(self):
        return {
            'form': self.form.cleaned_data,
            'teacher_forms': [form.cleaned_data for form in self.teacher_forms],
            'member_forms': [form.cleaned_data for form in self.member_forms],
        }

    def forms(self):
        return {
            'form': self.form,
            'teacher_forms': self.teacher_forms,
            'member_forms': self.member_forms,
            'errors': [self.form.errors] +
                [form.errors for form in self.teacher_forms] +
                [form.errors for form in self.member_forms]
        }

    def prepare_members(self, data):
        members = []
        for no in range(0, self.member_size):
            member = {}
            for field in self.member_field:
                member[field] = data.get('member-{no}-{field}'.format(no=no, field=field))
            members.append(member)
        return members


class ReviewForm(ReviewValidMixin, ReviewSaveMixin, forms.Form):
    jury = forms.ModelChoiceField(queryset=get_user_model().objects.get_queryset())
    team = forms.ModelChoiceField(queryset=Team.objects.calc())
    is_copy = forms.NullBooleanField()
    is_suggest = forms.NullBooleanField()
    score = forms.DecimalField(max_digits=5, decimal_places=2)
    comment = forms.CharField(required=False)

    def clean(self, *args, **kwargs):
        cleaned_data = super(ReviewForm, self).clean(*args, **kwargs)
        self.valid_extra(cleaned_data)
        return cleaned_data


class ReviewForms(object):
    def __init__(self, data, request):
        self.request = request
        reviews = self.prepare(data)
        self.forms = [ReviewForm(review) for review in reviews]

    def prepare(self, data):
        reviews = []
        for i in range(1, self.get_size(data)+1):
            reviews.append(dict(
                team=data['team_id-'+str(i)],
                jury=get_user_model().objects.filter(pk=self.request.user.pk),
                is_copy=True if data.get('is_copy-'+str(i), None) else False,
                is_suggest=True if data.get('is_suggest-'+str(i), None) else False,
                score=data['score-'+str(i)],
                comment=data['comment-'+str(i)],
            ))
        return reviews

    def is_valid(self):
        is_pass = True
        for form in self.forms:
            if not form.is_valid():
                is_pass = False
        return is_pass

    def save(self):
        for form in self.forms:
            form.save()

    def errors(self):
        return [form.errors for form in self.forms]

    @staticmethod
    def get_size(data):
        return len([val for key, val in data.iteritems() if key.startswith('team_id-')])
