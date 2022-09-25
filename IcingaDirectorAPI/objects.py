# -*- coding: utf-8 -*-
"""
Icinga Director API client base
"""

import logging

from IcingaDirectorAPI.base import Base
from IcingaDirectorAPI.exceptions import IcingaDirectorApiException

LOG = logging.getLogger(__name__)


class Objects(Base):
    """
    Icinga 2 API objects class
    """

    base_url_path = 'icingaweb2/director'

    @staticmethod
    def _convert_object_type(object_type=None, mode='multi'):
        """
        check if the object_type is a valid Icinga Director object type
        """

        type_conv = {
            'Command': ['commands', 'command?name='],
            'CommandTemplate': ['commands', 'command?name='],
            'Endpoint': ['endpoints', 'endpoint?name='],
            'Host': ['hosts', 'host?name='],
            'HostGroup': ['hostgroups', 'hostgroup?name='],
            'HostTemplate': ['hosts/templates', 'host?name='],
            'Notification': ['notifications/applyrules', 'notification?name='],
            'NotificationTemplate': ['notifications/templates', 'notification?name='],
            'Service': ['services', 'service?host=&name='],
            'ServiceApplyRule': ['services/applyrules', 'service?id='],
            'ServiceGroup': ['servicegroups', 'servicegroup?name='],
            'ServiceTemplate': ['services/templates', 'service?name='],
            'Timeperiod': ['timeperiods', 'timeperiod?name='],
            'TimeperiodTemplate': ['timeperiods/templates', 'timeperiod?name='],
            'User': ['users', 'user?name='],
            'UserGroup': ['usergroups', 'usergroup?name='],
            'UserTemplate': ['users/templates', 'user?name='],
            'Zone': ['zones', 'zone?name=']
        }

        if object_type not in type_conv:
            raise IcingaDirectorApiException(f'Icinga Director object type "{object_type}" does not exist.')

        if mode == 'multi':
            return type_conv[object_type][0]
        elif mode == 'single':
            return type_conv[object_type][1]
        else:
            raise IcingaDirectorApiException(f'API request mode "{mode}" does not exist.')

    def get(self,
            object_type,
            name):
        """
        get object of given type by given name

        :param object_type: type of the object
        :type object_type: string
        :param name: list object with this name
        :type name: string

        example 1:
        get('Host', 'webserver01.domain')

        example 2:
        get('Service', 'webserver01.domain!ping4')

        example 3:
        get('ServiceApplyRule', 'ping4')
        """

        object_type_url_path = self._convert_object_type(object_type, 'single')
        url_path = f'{self.base_url_path}/{object_type_url_path}{name}'

        if object_type == 'Service':

            if name.count('!') != 1:
                raise IcingaDirectorApiException(f'Service object must have form "hostname!servicename".')

            splitnames: list = name.split('!')
            object_type_url_path = object_type_url_path.replace('&', splitnames[0] + '&') + splitnames[1]
            url_path = f'{self.base_url_path}/{object_type_url_path}'

        return self._request('GET', url_path)['objects']

    def list(self,
             object_type,
             query=None):
        """
        list or filter all objects of given type (by name)

        :param object_type: type of the object
        :type object_type: string
        :param query: filters items by name
        :type query: string

        example 1:
        list('Host')

        example 2:
        list('NotificationTemplate')

        example 3:
        list('Host', query='webserver')
        """

        object_type_url_path = self._convert_object_type(object_type, 'multi')
        url_path = f'{self.base_url_path}/{object_type_url_path}'

        if query:
            url_path += f'?q={query}'

        return self._request('GET', url_path)['objects']

    def create(self,
               object_type,
               name,
               templates=None,
               attrs=None):
        """
        create an object

        :param object_type: type of the object
        :type object_type: string
        :param name: the name of the object
        :type name: string
        :param templates: templates used
        :type templates: list
        :param attrs: object's attributes
        :type attrs: dictionary

        example 1:
        create('Host', 'localhost', ['generic-host'], {'address': '127.0.0.1', 'vars': {'os': 'Linux'}})

        example 2:
        create('Service',
               'ping4',
               {'host': 'localhost', 'display_name': 'PING', 'check_command': 'ping4'},
               ['generic-service'])
        """

        object_type_url_path = self._convert_object_type(object_type, 'single').split('?')[0]

        if object_type.endswith('Template'):
            object_type = 'template'
        else:
            object_type = 'object'

        payload: dict = {
            'object_name': name,
            'object_type': object_type,
        }

        if attrs:
            payload += attrs
        if templates:
            payload['imports'] = templates

        url_path = f'{self.base_url_path}/{object_type_url_path}'

        return self._request('POST', url_path, payload)

    def update(self,
               object_type,
               name,
               attrs):
        """
        update an object

        :param object_type: type of the object
        :type object_type: string
        :param name: the name of the object
        :type name: string
        :param attrs: object's attributes to change
        :type attrs: dictionary

        example 1:
        update('Host', 'localhost', {'address': '127.0.1.1'})

        example 2:
        update('Service', 'testhost3!dummy', {'check_interval': '10m'})
        """
        object_type_url_path = self._convert_object_type(object_type)
        url_path = f'{self.base_url_path}/{object_type_url_path}{name}'

        if object_type == 'Service':

            if name.count('!') != 1:
                raise IcingaDirectorApiException(f'Service object must have form "hostname!servicename".')

            splitnames: list = name.split('!')
            object_type_url_path = object_type_url_path.replace('&', splitnames[0] + '&') + splitnames[1]
            url_path = f'{self.base_url_path}/{object_type_url_path}'

        return self._request('POST', url_path, attrs)

    def delete(self,
               object_type,
               name=None):
        """
        delete an object

        :param object_type: type of the object
        :type object_type: string
        :param name: the name of the object
        :type name: string

        example 1:
        delete('Host', 'localhost')

        example 2:
        delete('Service', 'testhost3!dummy')
        """

        object_type_url_path = self._convert_object_type(object_type, 'single')
        url_path = f'{self.base_url_path}/{object_type_url_path}{name}'

        if object_type == 'Service':

            if name.count('!') != 1:
                raise IcingaDirectorApiException(f'Service object must have form "hostname!servicename".')

            splitnames: list = name.split('!')
            object_type_url_path = object_type_url_path.replace('&', splitnames[0] + '&') + splitnames[1]
            url_path = f'{self.base_url_path}/{object_type_url_path}'

        return self._request('DELETE', url_path)
