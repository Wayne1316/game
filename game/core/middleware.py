# -*- coding: utf-8 -*-
import logging

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class XForwardedForMiddleware(MiddlewareMixin):
    """Replace \`\`REMOTE_ADDR\`\` with \`\`HTTP_X_FORWARDED_FOR\`\`

    When reverse proxying from nginx, we receive a tcp connection from
    localhost which isn"t the client"s real ip address.  Normally
    reverse proxies are configured to set the \`\`X-Forwarded-For\`\`
    header which gives us the actual client ip.
    """

    logger = logging.getLogger('header')
    PRIVATE_IP_PREFIX = (
        '10.',
        '192.168.',
        '172.'
    )

    def write_log(self, key, val, level=logging.INFO):
        self.logger.log(level, '%s = %s' % (key, val))

    def process_request(self, request):
        for k in request.META.keys():
            self.write_log(k, request.META[k])
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            parts = x_forwarded_for.split(',')
            for temp_ip in parts:
                temp_ip = temp_ip.strip()
                if not temp_ip.startswith(self.PRIVATE_IP_PREFIX):
                    request.META['REMOTE_ADDR'] = temp_ip
                    break

    def process_exception(self, request, exception):
        self.write_log('', exception.message, logging.ERROR)
