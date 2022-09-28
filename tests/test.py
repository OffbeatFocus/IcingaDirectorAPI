# -*- coding: utf-8 -*-
"""
Icinga Director API functionality tests
"""
from time import sleep

from IcingaDirectorAPI.director import Director

director = Director('http://localhost:8080', 'icingaadmin', 'icinga')

test_objects: dict = {
    'Zone': {
        'z_test1': {
            'attrs': {'parent': 'master'}
        },
        'z_test2': {
            'attrs': {'parent': 'z_test1'}
        }
    },
    'Endpoint': {
        'e_test1': {
            'attrs': {'zone': 'z_test1'}
        },
        'e_test2': {
            'attrs': {'zone': 'z_test2'}
        }
    },
    'CommandTemplate': {
        'ct_test1': {
            'attrs': {
                'arguments': {
                    '-T': {
                        'description': 'Test',
                        'required': bool(1),
                        'value': 'Test'
                    },
                },
                'command': '/bin/true', 'methods_execute': 'PluginCheck', 'timeout': '1m'}
        },
        'ct_test2': {
            'templates': ['ct_test1'],
            'attrs': {'command': '/bin/false', 'methods_execute': 'PluginCheck', 'timeout': '30'}
        }
    },
    'Command': {
        'c_test1': {
            'attrs': {'command': '/bin/false', 'methods_execute': 'PluginCheck', 'timeout': '30'}
        },
        'c_test2': {
            'templates': ['ct_test1'],
            'attrs': {
                "arguments": {
                    "-T": {
                        "description": "Test",
                        "required": bool(1),
                        "value": "Test"
                    },
                },
                'command': '/bin/false', 'timeout': '30s'}
        },
        'c_notify': {
            'attrs': {
                "arguments": {
                    "-H": {
                        "description": "Hostname",
                        "required": bool(0),
                        "value": "$host.name$"
                    },
                    "-S": {
                        "description": "Servicename",
                        "required": bool(1),
                        "value": "$service.name$"
                    },
                    "-a": {
                        "description": "IP Address of Host",
                        "required": bool(0),
                        "value": "$address$"
                    }
                },
                'command': '/bin/true', 'methods_execute': 'PluginNotification', 'timeout': '1m'}
        }
    },
    'HostTemplate': {
        'ht_test1': {
            'attrs': {'check_command': 'c_test1', 'max_check_attempts': '3',
                      'vars': {'os': 'Linux'}}
        },
        'ht_test2': {
            'templates': ['ht_test1'],
            'attrs': {"accept_config": bool(0), "check_command": "c_test2", "check_interval": "3m",
                      "enable_active_checks": bool(0), "enable_event_handler": bool(1),
                      "enable_flapping": bool(1), "enable_notifications": bool(0),
                      "enable_passive_checks": bool(0), "enable_perfdata": bool(0),
                      "has_agent": bool(0), "master_should_connect": bool(1),
                      "max_check_attempts": "3", "retry_interval": "1m", 'vars': {'os': 'Windows'}}
        }
    },
    'Host': {
        'h_test1': {
            'templates': ['ht_test1'],
            'attrs': {}
        },
        'h_test2': {
            'templates': ['ht_test2', 'ht_test1'],
            'attrs': {"address": "10.237.226.185", "display_name": "webserver12.test.com",
                      "zone": "z_test1", 'vars': {'os': 'Linux', 'processorcount': '4'}}
        }
    },
    'HostGroup': {
        'hg_rhel7': {
            'attrs': {"assign_filter": "host.vars.os_family=\"RedHat\"&&host.vars.os_release=\"7\"",
                      "display_name": "RHEL 7"}
        },
        'hg_windows': {
            'attrs': {"assign_filter": "host.vars.os=\"Windows\"",
                      "display_name": "Windows"}
        }
    },
    'Timeperiod': {
        't_24x7': {
            'attrs': {'display_name': 'always',
                      'ranges': {'friday': '00:00-24:00',
                                 'monday': '00:00-24:00',
                                 'saturday': '00:00-24:00',
                                 'sunday': '00:00-24:00',
                                 'thursday': '00:00-24:00',
                                 'tuesday': '00:00-24:00',
                                 'wednesday': '00:00-24:00'}
                      }
        }
    },
    'UserTemplate': {
        'ut_test1': {
            'attrs': {'enable_notifications': bool(0), 'period': 't_24x7'}
        }
    },
    'User': {
        'u_test1': {
            'attrs': {'enable_notifications': bool(0), 'period': 't_24x7'}
        },
        'u_test2': {
            'templates': ['ut_test1'],
            'attrs': {'enable_notifications': bool(1)}
        }
    },
    'UserGroup': {
        'ug_test1': {
            'attrs': {'display_name': 'Test Group 1'}
        },
        'ug_test2': {
            'attrs': {'display_name': 'Test Group 2'}
        }
    },
    'NotificationTemplate': {
        'nt_test1': {
            'attrs': {'command': 'c_notify', 'notification_interval': '0',
                      'period': 't_24x7', 'states': ['Down', 'Up'],
                      'types': ['Custom', 'Problem', 'Recovery'],
                      'users': ['u_test1']}
        },
        'nt_test2': {
            'templates': ['nt_test1'],
            'attrs': {'states': ['Down'], 'users': ['u_test2']}
        }
    },
    'Notification': {
        'n_test1': {
            'templates': ['nt_test1'],
            'attrs': {
                'apply_to': 'service', 'assign_filter': 'host.vars.environment="build"'
            }
        },
        'n_test2': {
            'templates': ['nt_test2', 'nt_test1'],
            'attrs': {'apply_to': 'host', 'host_name': 'h_test2'}
        }
    },
    'ServiceTemplate': {
        # 'st_test1': {
        #     'attrs': {'check_command': 'c_test2', 'check_interval': '300',
        #               'enable_active_checks': bool(0), 'enable_event_handler': bool(0),
        #               'enable_notifications': bool(0), 'enable_passive_checks': bool(0),
        #               'enable_perfdata': bool(0), 'max_check_attempts': '3', 'retry_interval': '60',
        #               'use_agent': bool(1)}
        # },
        'st_test1': {
            'attrs': {'check_command': 'c_test2', 'check_interval': '300',
                      'max_check_attempts': '3', 'retry_interval': '60'}
        },
        'st_test2': {
            'templates': ['st_test1'],
            'attrs': {'max_check_attempts': '1'}
        }
    },
    'Service': {
        's_test1': {
            'templates': ['st_test2'],
            'attrs': {'check_command': 'c_test', 'display_name': 'Test Service',
                      'host': 'h_test1', 'vars': {'blub': 'blib'}}
        },
        's_test2': {
            'templates': ['st_test1'],
            'attrs': {}
        }
    },
    'ServiceApplyRule': {
        'sa_test1': {
            'templates': ['st_test2'],
            'attrs': {
                'assign_filter': 'host.name="h_test2"', 'check_command': 'c_test1',
                'display_name': 'Test ServiceApply'
            }
        }
    },
    'ServiceGroup': {
        'sg_test1': {
            'attrs': {'assign_filter': 'service.vars.testvar="Test"', 'display_name': 'Test Group'}
        }
    }
}


# --- DELETE
rev_types: dict = dict(reversed(list(test_objects.items())))
for object_type in rev_types:
    rev_objects: list = list(reversed(list(test_objects[object_type])))
    object_list: list = [o['object_name'] for o in director.objects.list(object_type)]
    for obj in rev_objects:
        if obj in object_list:
            print(f'trying to delete object {obj} ...')
            director.objects.delete(object_type, obj)

# --- CREATE
for object_type in test_objects:

    print(f'\n{object_type}:')

    object_list: list = [o['object_name'] for o in director.objects.list(object_type)]
    print(f'{object_list}')

    for obj in test_objects[object_type]:
        if obj not in object_list:
            print(f'trying to create object {obj} ...')

            if 'templates' not in test_objects[object_type][obj] \
                    and 'attrs' not in test_objects[object_type][obj]:
                print(director.objects.create(object_type, obj))

            elif 'attrs' not in test_objects[object_type][obj]:
                print(director.objects.create(object_type, obj, test_objects[object_type][obj]['templates']))

            elif 'templates' not in test_objects[object_type][obj]:
                print(director.objects.create(object_type, obj, attrs=test_objects[object_type][obj]['attrs']))

            else:
                print(director.objects.create(object_type, obj,
                                              test_objects[object_type][obj]['templates'],
                                              test_objects[object_type][obj]['attrs']))

        sleep(.5)

# --- LIST & GET

# --- MODIFY

# --- DELETE
