# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mimetypes
import os

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseNotModified, Http404
from django.shortcuts import render
from django.views.generic import View
from django.views.static import was_modified_since
from django.utils.http import http_date

from game.models import (
    Subject,
    Activity,
)


class SingleFileMixin(object):
    """
    Provides the ability to retrieve a single object for further manipulation.
    """
    model = None
    queryset = None
    field = None
    path = None
    pk_url_kwarg = 'pk'

    def get_path(self, queryset=None):
        """
        Returns the file's path.

        By default this requires `self.queryset` and a `pk`
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # If none of those are defined, it's an error.
        if pk is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            path = getattr(obj, self.field).path
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})

        return path

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.

        Note that this method is called by the default implementation of
        `get_path` and may not be called if `get_path` is overridden.
        """
        if self.queryset is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        return self.queryset.all()


class FileView(SingleFileMixin, View):
    """
    A base view for displaying a single object
    """
    def get(self, request, *args, **kwargs):
        if self.path is None:
            self.path = self.get_path()
        if not os.path.exists(self.path):
            raise Http404('"{path}" does not exist'.format(path=self.path))
        stat = os.stat(self.path)
        mimetype, encoding = mimetypes.guess_type(self.path)
        mimetype = mimetype or 'application/octet-stream'
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'), stat.st_mtime, stat.st_size):
            return HttpResponseNotModified(mimetype - mimetype)
        response = HttpResponse(open(self.path, 'rb').read(), content_type=mimetype)
        response['Last-Modified'] = http_date(stat.st_mtime)
        response['Content-Length'] = stat.st_size
        if encoding:
            response['Content-Encoding'] = encoding
        return response


def showip(request):
    return HttpResponse("REMOTE_ADDR:{remote_addr}\n<br/>X_FORWARDED_FOR:{x_forwarded_for}".format(
        remote_addr=request.META.get('REMOTE_ADDR'),
        x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR'),
    ))


def home(request):
    data = {
        'subjects': Subject.objects.all(),
        'annotated': Activity.objects.join().order_by('-start')[:4],
        'history': Activity.objects.history().order_by('-start')[:4],
    }
    return render(request, 'home.html', data)
