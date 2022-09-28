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
    def _get_endpoint(object_type: str,
                      mode: str) -> str:
        """
        validate object_type and return Icinga Director API endpoint
        """

        allowed_types = [
            'Command',
            'CommandTemplate',
            'Endpoint',
            'Host',
            'HostGroup',
            'HostTemplate',
            'Notification',
            'NotificationTemplate',
            'Service',
            'ServiceApplyRule',
            'ServiceGroup',
            'ServiceTemplate',
            'Timeperiod',
            'TimeperiodTemplate',
            'User',
            'UserGroup',
            'UserTemplate',
            'Zone'
        ]

        if object_type not in allowed_types:
            raise IcingaDirectorApiException(f'Icinga Director object type "{object_type}" does '
                                             f'not exist or is not supported yet).')

        if mode == 'list':
            if object_type.startswith('Command'):
                return 'commands'
            if object_type.endswith('Template'):
                return object_type.lower().replace('template', 's/templates')
            if object_type in ['Notification', 'ServiceApplyRule']:
                return object_type.replace('ApplyRule', '').lower() + 's/applyrules'
            return object_type.lower() + 's'

        if mode in ['create', 'delete', 'get', 'modify']:
            return object_type.lower().replace('template', '').replace('applyrule', '')

        raise IcingaDirectorApiException(f'API request mode "{mode}" does not exist. Allowed '
                                         f'values: ["create", "delete", "get", "list", "modify"]')

    @staticmethod
    def _get_selector(object_type: str,
                      name: str) -> str:
        """
        return object selector for given object_type
        """

        if object_type == 'Service':
            if name.count('!') != 1:
                raise IcingaDirectorApiException('Service object must have form '
                                                 '"hostname!servicename".')
            splitnames: list = name.split('!')
            return f'host={splitnames[0]}&name={splitnames[1]}'

        return f'name={name}'

    def get(self,
            object_type: str,
            name: str) -> dict:
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

        endpoint = self._get_endpoint(object_type, 'get')
        selector = self._get_selector(object_type, name)

        url_path = f'{self.base_url_path}/{endpoint}?{selector}'

        return self._request('GET', url_path)

    def list(self,
             object_type: str,
             query: str = None) -> list:
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

        object_type_url_path = self._get_endpoint(object_type, 'list')
        url_path = f'{self.base_url_path}/{object_type_url_path}'

        if query:
            url_path += f'?q={query}'

        if object_type == 'Command':
            return [c for c in
                    self._request('GET', url_path)['objects'] if c["object_type"] == "object"]

        if object_type == 'CommandTemplate':
            return [c for c in
                    self._request('GET', url_path)['objects'] if c["object_type"] == "template"]

        return self._request('GET', url_path)['objects']

    def create(self,
               object_type: str,
               name: str,
               templates: list = None,
               attrs: dict = None) -> dict:
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
        create('Host',
               'localhost',
               ['generic-host'],
               {'address': '127.0.0.1', 'vars': {'os': 'Linux'}})

        example 2:
        create('Service',
               'ping4',
               {'host': 'localhost', 'display_name': 'PING', 'check_command': 'ping4'},
               ['generic-service'])
        """

        endpoint: str = self._get_endpoint(object_type, 'create')

        url_path = f'{self.base_url_path}/{endpoint}'

        if object_type.endswith('Template'):
            object_type = 'template'
        elif object_type in ['Notification', 'ServiceApplyRule']:
            object_type = 'apply'
        else:
            object_type = 'object'

        payload: dict = {
            'object_name': name,
            'object_type': object_type,
        }

        if attrs:
            payload |= attrs
        if templates:
            payload['imports'] = templates

        return self._request('POST', url_path, payload)

    def modify(self,
               object_type: str,
               name: str,
               attrs: dict) -> dict:
        """
        modify an object

        :param object_type: type of the object
        :type object_type: string
        :param name: the name of the object
        :type name: string
        :param attrs: object's attributes to change
        :type attrs: dictionary

        example 1:
        modify('Host', 'localhost', {'address': '127.0.1.1'})

        example 2:
        modify('Service', 'testhost3!dummy', {'check_interval': '10m'})
        """
        endpoint: str = self._get_endpoint(object_type, 'modify')
        selector = self._get_selector(object_type, name)

        url_path = f'{self.base_url_path}/{endpoint}?{selector}'

        return self._request('POST', url_path, attrs)

    def delete(self,
               object_type: str,
               name: str) -> dict:
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

        endpoint = self._get_endpoint(object_type, 'delete')
        selector = self._get_selector(object_type, name)

        url_path = f'{self.base_url_path}/{endpoint}?{selector}'

        return self._request('DELETE', url_path)
