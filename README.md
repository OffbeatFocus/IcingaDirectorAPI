# IcingaDirectorAPI

IcingaDirectorAPI is a small module to interact with the [Icinga Director REST API](https://icinga.com/docs/icinga-director/latest/doc/70-REST-API/), written in [Python](http://www.python.org).

# Features

- simple authentication
- create, get, list, modify and delete Director Objects through object type, name and definition (in JSON/dict format)

# Usage

## Import

    from IcingaDirectorAPI.director import Director

## Authentication

For now only basic authentication (with username & password) is supported.
Example:

    director = Director('https://icinga-master.with-director.local:8080', 'username', 'password')

# Object methods

## Supported object types

For now:
- Command
- CommandTemplate
- Endpoint
- Host
- HostGroup
- HostTemplate
- Notification
- NotificationTemplate
- Service
- ServiceApplyRule
- ServiceGroup
- ServiceTemplate
- Timeperiod
- TimeperiodTemplate
- User
- UserGroup
- UserTemplate
- Zone


## list()

To get a list of all objects of the same type use the funtion `objects.list()`.

| Parameter    | Type   | Description                           |
|--------------|--------|---------------------------------------|
| object\_type | string | **Required.** The object type to get. |

Examples:

Get all hosts:

    client.objects.list('Host')

Get all timeperiods:

    client.objects.list('Timeperiod')


## get()

To get a single object use the function `objects.get()`.

| Parameter    | Type   | Description                           |
|--------------|--------|---------------------------------------|
| object\_type | string | **Required.** The object type to get. |
| name         | string | **Required.** The object's name.      |

Examples:

Get host `webserver01.domain`:

    director.objects.get('Host', 'webserver01.domain')

Get service `ping4` of host `webserver01.domain`:

    director.objects.get('Service', 'webserver01.domain!ping4')

Get notification template `mail_notifs`:

    director.objects.get('NotificationTemplate', 'mail_notifs')


## create()

Create an object using `templates` and specify attributes (`attrs`).

| Parameter    | Type       | Description                                  |
|--------------|------------|----------------------------------------------|
| object\_type | string     | **Required.** The object's type.             |
 | name         | string     | **Optional.** The objects name.              |
 | templates    | list       | **Optional.** A list of templates to import. |
 | attrs        | dictionary | **Optional.** The objects attributes.        |

Examples:

Create a host:

    director.objects.create(
        'Host',
        'localhost',
        ['generic-host'],
        {'address': '127.0.0.1'})

Create a service for Host "localhost":

    director.objects.create(
        'Service',
        'localhost!Ping',
        ['generic-service'],
        {'check_command': 'ping4'})

Create a notification template:

    director.objects.create(
        'NotificationTemplate',
        'nt_host-to-jira',
        attrs={'command': 'c_notify', 'notification_interval': '0',
               'period': 't_24x7', 'states': ['Down', 'Up'],
               'types': ['Custom', 'Problem', 'Recovery'], 'users': ['u_jira']})

Notice the addition of the `attrs=` selector, when skipping the optional templates parameter.
If other objects are referenced through the JSON/dict definition, they have to exist in advance of executing this command, since Director does a built-in lookup for these objects.


## modify()

Modify attributes of an existing object.

| Parameter    | Type       | Description                                                   |
|--------------|------------|---------------------------------------------------------------|
| object\_type | string     | **Required.** The object type to get, e.g. `Host`, `Service`. |
| name         | string     | **Optional.** The objects name.                               |
| attrs        | dictionary | **Optional.** The objects attributes.                         |

Examples:

Change the ip address of a host:

    client.objects.update(
        'Host',
        'localhost',
        {'address': '127.0.1.1'})

Update a service and change the check interval:

    client.objects.create('Service',
           'localhost!dummy',
           ['generic-service'],
           {'check_interval': '10m'})


## <a id="objects-delete"></a> objects.delete()

Update an object with the specified attributes.

  Parameter     | Type       | Description
  --------------|------------|--------------
  object\_type  | string     | **Required.** The object type to get, e.g. `Host`, `Service`.
  name          | string     | **Optional.** The objects name.
  filters       | string     | **Optional.** Filter expression for matching the objects.
  filter\_vars  | dictionary | **Optional.** Variables which are available to your filter expression.
  cascade       | boolean    | **Optional.** Also delete dependent objects. Defaults to `True`.

Examples:

Delete the "localhost":

    client.objects.delete('Host', 'localhost')

Delete all services matching `vhost\*`:

    client.objects.delete('Service', filters='match("vhost\*", service.name)')