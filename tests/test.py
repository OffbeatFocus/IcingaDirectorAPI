# -*- coding: utf-8 -*-
"""
Icinga Director API functionality tests
"""

from test_objects import test_objects
from IcingaDirectorAPI.director import Director  # pylint: disable=import-error

# default credentials & localhost for testing, e.g. with a local container
director = Director('http://localhost', 'icingaadmin', 'icinga')

# --- CREATE / GET / LIST
for object_type, objects in test_objects.items():

    print(f'\n{object_type}:')

    object_list: list = [o['object_name'] for o in director.objects.list(object_type)]
    print(f'list: {object_list}')

    for object_name, object_definition in objects.items():
        if object_name not in object_list:
            print(f'trying to create object {object_name} ...')

            if 'templates' not in object_definition and 'attrs' not in object_definition:
                director.objects.create(object_type, object_name)

            elif 'attrs' not in object_definition:
                director.objects.create(object_type, object_name, object_definition['templates'])

            elif 'templates' not in object_definition:
                director.objects.create(object_type, object_name, attrs=object_definition['attrs'])

            else:
                director.objects.create(object_type, object_name,
                                        object_definition['templates'],
                                        object_definition['attrs'])
        else:
            print(f'trying to get object {object_name} ...')
            if object_type == 'Service':
                hostname: str = object_definition['attrs']['host']
                director.objects.get(object_type, f'{hostname}!{object_name}')
            else:
                director.objects.get(object_type, object_name)

# --- MODIFY
print('\n\ntrying to modify object z_test2 ...')
director.objects.modify('Zone', 'z_test2', {'parent': 'master'})

print('trying to modify object e_test2 ...')
director.objects.modify('Endpoint', 'e_test2', {'zone': 'z_test1'})

print('trying to modify object ct_test2 ...')
director.objects.modify('CommandTemplate', 'ct_test2', {'command': '/bin/true'})

print('trying to modify object c_test1 ...')
director.objects.modify('Command', 'c_test1', {'command': '/bin/true'})

print('trying to modify object ht_test1 ...')
director.objects.modify('HostTemplate', 'ht_test1', {'max_check_attempts': '4'})

print('trying to modify object h_test1 ...')
director.objects.modify('Host', 'h_test1', {'vars': {'os': 'Linux', 'processorcount': '24'}})

print('trying to modify object hg_windows ...')
director.objects.modify('HostGroup', 'hg_windows', {'display_name': 'Windows Hosts'})

print('trying to modify object t_24x7 ...')
director.objects.modify('Timeperiod', 't_24x7', {'display_name': 'day and night'})

print('trying to modify object ut_test1 ...')
director.objects.modify('UserTemplate', 'ut_test1', {'enable_notifications': bool(0)})

print('trying to modify object u_test2 ...')
director.objects.modify('User', 'u_test2', {'display_name': 'hehe'})

print('trying to modify object ug_test1 ...')
director.objects.modify('UserGroup', 'ug_test1', {'display_name': 'Better Test Group'})

print('trying to modify object nt_test2 ...')
director.objects.modify('NotificationTemplate', 'nt_test2', {'states': ['Up', 'Down']})

print('trying to modify object n_test1 ...')
director.objects.modify('Notification', 'n_test1', {'notification_interval': '3h'})

print('trying to modify object st_test2 ...')
director.objects.modify('ServiceTemplate', 'st_test2', {'vars': {'testvar': 'Test'}})

print('trying to modify object s_test1 ...')
director.objects.modify('Service', 'h_test1!s_test1', {'vars': {'blub': 'blab'}})

print('trying to modify object sa_test1 ...')
director.objects.modify('ServiceApplyRule', 'sa_test1', {'vars': {'testvar': 'Test'}})

print('trying to modify object sg_test1 ...')
director.objects.modify('ServiceGroup', 'sg_test1', {'display_name': 'Best Test Group'})

# --- DELETE
rev_types: dict = dict(reversed(list(test_objects.items())))
for object_type, objects in rev_types.items():

    print(f'\n{object_type}:')

    rev_objects: list = list(reversed(list(objects)))
    object_list: list = [o['object_name'] for o in director.objects.list(object_type)]
    print(f'list: {object_list}')
    for object_name in rev_objects:
        if object_name in object_list:
            print(f'trying to delete object {object_name} ...')
            if object_type == 'Service':
                hostname: str = test_objects['Service'][object_name]['attrs']['host']
                director.objects.delete(object_type, f'{hostname}!{object_name}')
            else:
                director.objects.delete(object_type, object_name)
