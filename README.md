<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/C15HOT/yandex_smart_home_api">
    <img src="docs/images/img.png" alt="Logo" width="50%" height="50%">
  </a>

<h3 align="center">Yandex Smart Home API</h3>

  <p align="center">
    Asynchronous library for working with the Yandex Device Control Protocol and yandex speakers with Alice.
  </p>
</div>

## About

The library contains methods for obtaining information about the smart home, smart home devices and managing these
devices.
Library methods allow you to separately manage smart home devices using the YandexApi class. The YandexSession/YandexSessionAsync class is used to control smart speakers.
The library provides convenient direct access to device objects that allow you to access device-accessible methods
## Built With

* [![Python][python-shield]][python-url]

## Getting started

### Requirements
<details><summary>Install requirements</summary>

```sh
pip install -r requirements.txt
```
```
aiofiles==22.1.0
aiohttp==3.8.3
aiohttp-socks==0.7.1
aiosignal==1.3.1
anyio==3.6.2
async-generator==1.10
async-timeout==4.0.2
attrs==22.2.0
certifi==2022.12.7
cffi==1.15.1
charset-normalizer==2.1.1
choicelib==0.1.5
exceptiongroup==1.1.0
frozenlist==1.3.3
h11==0.14.0
idna==3.4
multidict==6.0.3
outcome==1.2.0
pycparser==2.21
PySocks==1.7.1
python-dotenv==0.21.0
python-socks==2.1.1
requests==2.28.2
selenium==4.7.2
sniffio==1.3.0
sortedcontainers==2.4.0
trio==0.22.0
trio-websocket==0.9.2
typing_extensions==4.4.0
urllib3==1.26.13
vbml==1.1.post1
watchfiles==0.18.1
wsproto==1.2.0
yarl==1.8.2
```
</details>

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
from yandex_smart_home_api.api import YandexApi

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
from yandex_smart_home_api.devices import YandexSession

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
my_station.update_scenario(scenario_id='',
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

The application was developed within the framework of the research project "Development of algorithms for integrating the external environment of users into the ecosystem of their digital assistants" No. 622265)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python-shield]: https://img.shields.io/badge/Python-%203.9-blue?style=for-the-badge&logo=python
[python-url]: https://www.python.org/downloads/release/python-390
