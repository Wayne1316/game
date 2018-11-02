import os

from django.conf import settings

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class AnalyticsReporting(object):
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    KEY_FILE_LOCATION = settings.GOOGLE_ANALYTICS_API_JSON_LOCATION
    VIEW_ID = settings.GOOGLE_ANALYTICS_VIEW_ID

    def __init__(self):
        """Initializes an Analytics Reporting API V4 service object.

        Returns:
        An authorized Analytics Reporting API V4 service object.
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.KEY_FILE_LOCATION, self.SCOPES)

        # Build the service object.
        self.service = build('analyticsreporting', 'v4', credentials=credentials)

    def get_report(self, date_ranges, metrics):
        """Queries the Analytics Reporting API V4.

        Args:
        analytics: An authorized Analytics Reporting API V4 service object.
        Returns:
        The Analytics Reporting API V4 response.
        """
        return self.service.reports().batchGet(
            body={
                'reportRequests': [{
                    'viewId': self.VIEW_ID,
                    'dateRanges': date_ranges,
                    'metrics': metrics,
                }]
            }
        ).execute()

    def get_visits_report(self, start, end):
        response = self.get_report(
            date_ranges=[{'startDate': start, 'endDate': end}],
            metrics=[{'expression': 'ga:users'}, ]
        )
        return response['reports'][0]

    def get_visits(self, start, end):
        report = self.get_visits_report(start, end)
        context = self.format(report)
        return context['ga:users']

    @staticmethod
    def format(report):
        """
        format of report
        :param report:
        :return: dict of metrics
        """
        context = {}
        column_header = report.get('columnHeader', {})
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            ranges = row.get('metrics', [])

            for i, values in enumerate(ranges):
                for metric_header, value in zip(metric_headers, values.get('values')):
                    context[metric_header.get('name')] = value
        return context
