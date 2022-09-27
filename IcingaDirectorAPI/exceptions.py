# -*- coding: utf-8 -*-
"""
Icinga Director API client exceptions
"""


class IcingaDirectorApiException(Exception):
    """
    Icinga Director API exception class
    """

    def __init__(self, error):
        super().__init__(error)
        self.error = error

    def __str__(self):
        return str(self.error)


class IcingaDirectorApiRequestException(IcingaDirectorApiException):
    """
    Icinga Director API Request exception class
    """
    response = {}

    def __init__(self, error, response):
        super().__init__(error)
        self.response = response
