![img.png](img.png)

# Yandex Smart Home API

## About

Asynchronous library for working with the Yandex Device Control Protocol and yandex speakers with Alice.

The library contains methods for obtaining information about the smart home, smart home devices and managing these
devices

## Built With

[![img_1.png](img_1.png)](https://www.python.org)

## Getting started

### Prerequisites

Before you start, you need to register your application with the [yandex authentication system](https://oauth.yandex.ru)

After that, using the received token, following
the [instruction](https://yandex.ru/dev/id/doc/dg/oauth/concepts/about.html), you need to get the client_token to work
with the API

### Installation

  ```sh
  git clone https://github.com/C15HOT/yandex_smart_home_api
  ```

## Usage

### Smart devices

You must create an instance of the Yandex API class by specifying in the client_token attribute a token received by
instructions

```python
from api import YandexApi

api = YandexApi(client_token=client_token)
```

#### Examples

###### Getting Smart Home Information

```python
api.get_smart_home_info()
```

To simplify the operation, direct access to devices is implemented by creating an instance of the device class, and also
to methods available for devices, obtaining properties, abilities and information about the device.

(Note that all methods except set_id are asynchronous)

###### Getting device information and device management

```python
my_purifer = api.purifer.set_id(device_id='')
my_purifer.info()
my_purifer.on_off(value=True)

my_vacuum_cleaner = api.purifer.set_id(device_id='')
my_vacuum_cleaner.get_capabilities()
my_vacuum_cleaner.mode(value='turbo')

```

### Yandex smart speakers

You must create an instance of the YandexSession or YandexSessionAsync class by specifying the column id, obtained using
the above methods, as well as the login and password from the Yandex account.

```python
from devices import YandexSession

my_station = YandexSession(login='', password='', station_id='')

```

In the future, examples will be discussed for the synchronous class YandexSession, all actions for asynchronous
YandexSessionAsync is similar except that these methods must be used asynchronously. In addition, the use of a session
is different when using an asynchronous class, so you must call the asynchronous authorization method before executing
methods:

```python
my_station.authorize()
```

All control of the column is carried out using scripts. You can obtain default and added scripts using the method:

```python
my_station.add_scenario(scenario_name='',
                        activation_command='',
                        instance='',
                        value='')
```

scenario_name - script name activation_command - voice command for script activation in Alice instance - takes the
values of:

'text _ action '- to perform the action specified in the value

'phrase _ action '- to voice the text specified in the value

value - action or phrase depending on the instance type

To update the script, use the method:

```python
my_station.update_scenatio(scenario_id='',
                           scenario_name='',
                           activation_command='',
                           instance='',
                           value='')
```

To execute the script, use the method:

```python
my_station.exec_scenario(scenario_id='')
```

To delete a script, use the method:

```python
my_station.delete_scenario(scenario_id='')
```

#### Examples

###### Create and execute scenario

```python
from asyncio import get_event_loop
loop = get_event_loop()

ys = YandexSessionAsync(login='login', password='password', station_id='3333333-0700-4e50-a82d-999d9999v9999')

loop.run_until_complete(ys.authorize())
loop.run_until_complete(ys.add_scenario(scenario_name='purifer',
                       activation_command='purifer',
                       instance='text_action',
                       value='выключи очиститель воздуха'))
scenarios = loop.run_until_complete(ys.get_scenarios())
scenario_id = [scenario['id'] for scenario in scenarios if scenario['name'] == 'purifer'][0]
loop.run_until_complete(ys.exec_scenario(scenario_id=scenario_id))
loop.run_until_complete(ys.delete_scenario(scenario_id=scenario_id))


```

## Documentation

The library documentation is available in the [Github wiki](https://github.com/C15HOT/yandex_smart_home_api/wiki) of
this repository. There you can find instructions for using the methods, as well as all technical information about the
project.

## Contact

If you have any questions or comments on the project, email the developer - wvxp@mail.ru

## Acknowledgments

[comment]: <> (The application was developed within the framework of the research project "Development of mechanisms for designing the processes of users' vital activity into the ecosystem of their digital assistants" No. 621308)