from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.GameDetailView.as_view(), name='detail'),
    url(r'^history/$', views.HistoryListView.as_view(), name='history_list'),
    url(r'^(?P<pk>\d+)/history$', views.HistoryDetailView.as_view(), name='history_detail'),
    url(r'^history/(?P<pk>\d+)/team$', views.HistoryTeamView.as_view(), name='history_team'),
    url(r'^history/(?P<pk>\d+)/download$', views.HistoryFileView.as_view(), name='history_file'),
    url(r'^(?P<pk>\d+)/join$', views.JoinView.as_view(), name='join'),
    url(r'^achievement/$', views.AchieveListView.as_view(), name='achievement_list'),
    url(r'^achievement/(?P<pk>\d+)/comment$', views.AchieveDetailView.as_view(), name='achievement_comment'),
    url(r'^achievement/(?P<pk>\d+)/performance$', views.AchievePerformanceView.as_view(), name='achievement_performance'),
    url(r'^achievement/(?P<pk>\d+)/download$', views.AchieveFileView.as_view(), name='achievement_download'),
    url(r'^jury/$', views.JuryListView.as_view(), name='jury_list'),
    url(r'^jury/(?P<pk>\d+)$', views.JuryView.as_view(), name='jury'),
    url(r'^jury/(?P<pk>\d+)/review$', views.TeamReviewDetailView.as_view(), name='jury_review'),
    url(r'^jury/(?P<pk>\d+)/download$', views.TeamReviewFileView.as_view(), name='jury_file'),
]
