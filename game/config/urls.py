"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url

from rest_framework import routers

from .admin import admin_site
from core import views as core_views
from game import views as game_views


router = routers.DefaultRouter()
router.register(r'subject', game_views.SubjectViewSet)
router.register(r'activity', game_views.ActivityViewSet)


urlpatterns = [
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^nimdateehsylf/', admin_site.site.urls),
    url(r'^ip$', core_views.showip),
    url(r'^$', core_views.home, name='home'),
    url(r'^game/', include('game.urls', namespace='game')),
    url('^', include('users.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

