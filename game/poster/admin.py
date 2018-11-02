# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64

from django.conf.urls import url
from django.contrib import admin
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, View

from . import models, forms


class PosterAdmin(admin.ModelAdmin):
    list_display = ('title', 'print_poster', )
    readonly_fields = ('print_poster', )
    form = forms.PosterForm

    def get_urls(self):
        urls = super(PosterAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/preview/$', self.PosterPreview.as_view(), name='poster_preview'),
            url(r'^(?P<pk>\d+)/print/$', self.PrintView.as_view(), name='poster_print'),
        ]
        return my_urls + urls

    class PosterPreview(DetailView):
        model = models.Poster

        def get_template_names(self):
            return "poster/{orientation}.html".format(orientation=self.object.style.orientation)

    class PrintView(DetailView):
        model = models.Poster
        template_name = 'poster/print.html'

    @staticmethod
    def print_poster(obj):
        if obj.id is not None:
            return format_html(
                '<a class="button" href="{url}" target="_blank">{title}</a>',
                url=reverse('admin:poster_print', kwargs={'pk': obj.id}),
                title=_('poster print'),
            )
        return ''


class TempAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(TempAdmin, self).get_urls()
        my_urls = [
            url(r'^create/$', self.CreateView.as_view(), name='temp_create'),
        ]
        return my_urls + urls

    class CreateView(View):
        def post(self, request):
            try:
                mime, blob = self.request.POST.get('image').split(';base64,')
                filename = 'poster.{extension}'.format(extension=mime.split('/')[-1])
                data = ContentFile(base64.b64decode(blob), name=filename)
                obj = models.Temp(file=data)
                obj.save()
                return JsonResponse({'status': 'success', 'redirect': obj.file.url})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': e.message})


admin.site.register(models.Temp, TempAdmin)
admin.site.register(models.Poster, PosterAdmin)
admin.site.register(models.Style)

