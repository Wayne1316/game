# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from rest_framework import serializers

from core.helper import get_site_uri
from . import models


class SubjectSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = models.Subject
        fields = ('title', 'link')

    def get_link(self, obj):
        return "{uri}{path}?subject={filter_id}".format(
            uri=get_site_uri(self.context['request']),
            path=reverse('game:history_list'),
            filter_id=obj.id
        )


class ActivitySerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = models.Activity
        fields = ('title', 'link')

    def get_link(self, obj):
        return "{uri}{path}".format(
            uri=get_site_uri(self.context['request']),
            path=reverse('game:detail', kwargs={'pk': obj.id}),
        )
