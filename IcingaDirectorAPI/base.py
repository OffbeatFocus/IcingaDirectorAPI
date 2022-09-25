# -*- coding: utf-8 -*-
"""
Icinga Director API client base
"""

import logging
import requests
from urllib.parse import urljoin
from exceptions import *

LOG = logging.getLogger(__name__)


class Base(object):
    """
    Icinga Director API Base Class
    """

    base_url_path = None

    def __init__(self, manager):
        """
        initialize object
        """

        self.manager = manager

    def _create_session(self, method='POST'):
        """
        create a session object
        """

        session = requests.Session()
        session.auth = (self.manager.username, self.manager.password)
        session.headers = {
            'User-Agent': 'Python-icingadirectorapi/{0}'.format(self.manager.version),
            'X-HTTP-Method-Override': method.upper(),
            'Accept': 'application/json'
        }

        return session

    def _request(self, method, url_path, payload=None):
        """
        make the request and return the body

        :param method: the HTTP method
        :type method: string
        :param url_path: the requested url path
        :type url_path: string
        :param payload: the payload to send
        :type payload: dictionary
        :returns: the response as json
        :rtype: dictionary
        """

        request_url = urljoin(self.manager.url, url_path)
        LOG.debug("Request URL: %s", request_url)

        # create session
        session = self._create_session(method)

        # create arguments for the request
        request_args = {
            'url': request_url,
            'verify': False
        }
        if payload:
            request_args['json'] = payload

        # do the request
        response = session.post(**request_args)

        if not 200 <= response.status_code <= 299:
            raise IcingaDirectorApiRequestException(
                'Request "{}" failed with status {}: {}'.format(
                    response.url,
                    response.status_code,
                    response.text,
                ), response.json())

        return response.json()
