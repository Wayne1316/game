from celery import Celery

from . import models, google_analytics_api


app = Celery()


@app.task
def visits_update():
    api = google_analytics_api.AnalyticsReporting()
    visits = api.get_visits('2018-10-01', 'today')
    models.Visit.objects.create(quantity=visits)
    return True
