# -*- coding: utf-8 -*-
"""
Icinga Director API client base
"""

import logging

from IcingaDirectorAPI.exceptions import IcingaDirectorApiException
from IcingaDirectorAPI.objects import Objects
from IcingaDirectorAPI import __version__

LOG = logging.getLogger(__name__)


class Director:  # pylint: disable=too-few-public-methods
    """
    Icinga Director Client class
    """

    def __init__(self,
                 url=None,
                 username=None,
                 password=None,
                 timeout=None):
        """
        initialize object
        """
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.objects = Objects(self)
        self.version = __version__

        if not self.url:
            raise IcingaDirectorApiException('No "url" defined.')
        if not self.username or not self.password:
            raise IcingaDirectorApiException('username and/or password not defined.')
