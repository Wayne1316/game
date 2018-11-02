# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator

from rest_framework import viewsets

from core.views import FileView
from .decorator import join_required, has_jury_data
from .form import JoinForm, ReviewForms
from .models import Activity, Subject, Team, Member, Review, GroupSetting
from . import serializers


class GameDetailView(DetailView):
    queryset = Activity.objects.join()
    template_name = 'game/detail.html'


class JoinView(View):
    @staticmethod
    def get_template(template):
        return 'game/join/{template}.html'.format(template=template)

    @method_decorator(login_required)
    @join_required
    def dispatch(self, request, *args, **kwargs):
        return super(JoinView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        obj = Activity.objects.get(pk=pk)
        context = {'object': obj}
        return render(request, self.get_template(obj.form), context)

    @transaction.atomic
    def post(self, request, pk):
        obj = Activity.objects.join(groupsetting__id=request.POST.get('group'))[0]
        context = {'object': obj, 'data': request.POST}
        form = JoinForm(activity=obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data()
            cleaned_data['form']['owner'] = request.user
            team = Team.objects.create(**cleaned_data['form'])
            for data in cleaned_data['teacher_forms']:
                data.update({'team': team})
                Member.objects.create(**data)
            if obj.form == 'thesis':
                for data in cleaned_data['member_forms']:
                    data.update({'team': team})
                    Member.objects.create(**data)
            return redirect(reverse('home'))
        context.update(form.forms())
        return render(request, self.get_template(obj.form), context)


class AchieveListView(ListView):
    paginate_by = 10
    template_name = 'game/achieve_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AchieveListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Team.objects.owner(self.request.user)
        return qs


class AchievePerformanceView(DetailView):
    template_name = 'game/achieve_performance.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AchievePerformanceView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Team.objects.owner(self.request.user)
        return qs


class AchieveDetailView(DetailView):
    template_name = 'game/achieve_comment.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AchieveDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Team.objects.owner(self.request.user, group__activity__status='close')
        return qs

    def get_context_data(self, **kwargs):
        context = super(AchieveDetailView, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(team=self.object)
        return context


class AchieveFileView(FileView):
    field = 'file'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AchieveFileView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = Team.objects.filter(owner=self.request.user)
        return qs


class JuryListView(ListView):
    paginate_by = 10
    template_name = 'game/jury_list.html'

    @method_decorator(login_required)
    @method_decorator(permission_required('game.review', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(JuryListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = GroupSetting.objects.jury(self.request.user)
        return qs


class JuryView(View):
    template = 'game/jury.html'

    @method_decorator(login_required)
    @method_decorator(permission_required('game.review', raise_exception=True))
    @method_decorator(has_jury_data)
    def dispatch(self, request, *args, **kwargs):
        return super(JuryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        context = self.get_context_data(pk)
        return render(request, self.template, context=context)

    def post(self, request, pk):
        forms = ReviewForms(request.POST, request)
        if forms.is_valid():
            forms.save()
            return redirect(reverse('game:jury', kwargs={'pk': pk}))
        else:
            context = self.get_context_data(pk)
            context['forms'] = forms.forms
            context['errors'] = forms.errors()
            return render(request, self.template, context=context)

    def get_context_data(self, pk):
        context = dict()
        context['object'] = GroupSetting.objects.jury(self.request.user, pk=pk).first()
        context['teams'] = Team.objects.review_group(pk, self.request.user)
        return context


class TeamReviewDetailView(DetailView):
    template_name = 'game/review_detail.html'

    @method_decorator(login_required)
    @method_decorator(permission_required('game.review', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TeamReviewDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Team.objects.review(self.request.user)
        return qs


class TeamReviewFileView(FileView):
    field = 'file'

    @method_decorator(login_required)
    @method_decorator(permission_required('game.review', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TeamReviewFileView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Team.objects.review(self.request.user)
        return qs


class HistoryListView(ListView):
    queryset = Activity.objects.history().order_by('-start')
    paginate_by = 10
    template_name = 'history/list.html'

    def get_queryset(self):
        qs = super(HistoryListView, self).get_queryset()

        # 主題篩選
        try:
            subject_id = self.request.GET.get('subject', None)
            if subject_id is not None and isinstance(int(subject_id), int):
                qs = qs.filter(subject__id=subject_id)
        except Exception:
            raise Http404

        # 查詢標題
        keyword = self.request.GET.get('keyword', None)
        if keyword is not None:
            qs = qs.filter(title__icontains=keyword)

        return qs

    def get_context_data(self, **kwargs):
        context = super(HistoryListView, self).get_context_data(**kwargs)
        subject_id = self.request.GET.get('subject', None)
        if subject_id is not None:
            context['subject'] = Subject.objects.get(pk=subject_id)
        return context


class HistoryDetailView(DetailView):
    queryset = Activity.objects.history()
    template_name = 'history/detail.html'

    def get_context_data(self, **kwargs):
        context = super(HistoryDetailView, self).get_context_data(**kwargs)
        context['teams'] = Team.objects.active(
            group__activity=self.kwargs.get(self.pk_url_kwarg),
            group__activity__is_show_form=True
        ).order_by('-group__priority', '-award__priority')
        return context


class HistoryTeamView(DetailView):
    queryset = Team.objects.history()
    template_name = 'history/team.html'


class HistoryFileView(FileView):
    field = 'file'
    queryset = Team.objects.history()


class SubjectViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer


class ActivityViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Activity.objects.join()
    serializer_class = serializers.ActivitySerializer
