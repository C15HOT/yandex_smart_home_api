# Yandex Smart Home API

### Что делает

Асинхронная библиотека для работы с Протоколом программного управления устройствами Яндекса, а также колонками с Алисой.

### Установка зависимостей

```
pip install -r requirements.txt
```

## Как пользоваться

### Управление умными устройствами

Необходимо создать экземпляр класса Yandex API, указав в атрибуте client_token токен, полученный по
инструкции (https://yandex.ru/dev/dialogs/smart-home/doc/concepts/platform-protocol.html)

```python
from api import YandexApi

api = YandexApi(client_token=token)
```

Класс YandexApi позволяет напрямую обращаться к методам API, описанным в инструкции.

#### Пример:

```python
api.get_smart_home_info()
api.get_device_info(device_id='')
```

Для упрощения работы реализован непосредственный доступ к устройствам путем создания экземпляра класса устройства, а
также к доступным для устройств методам, получению свойств, способностей и информации об устройстве.

#### Пример:

(Необходимо учитывать, что все методы, за исключением set_id, являются асинхронными)

```python
my_purifer = api.purifer.set_id(device_id='')
my_purifer.info()
my_purifer.on_off(value=True)

my_vacuum_cleaner = api.purifer.set_id(device_id='')
my_vacuum_cleaner.get_capabilities()
my_vacuum_cleaner.mode(value='turbo')

```

### Управление Яндекс колонками с Алисой

Необходимо создать экземпляр класса YandexSession или YandexSessionAsync (Асинхронная версия), указав id колонки,
полученный с помощью вышеуказанных методов, а также логин и пароль от аккаунта Яндекс.

```python
from devices import YandexSession

my_station = YandexSession(login='', password='', station_id='')

```

В дальнейшем примеры будут рассмотрены для синхронного класса YandexSession, все действия для асинхронного
YandexSessionAsync аналогичны, за исключением необходимости асинхронного использования этих методов.
Кроме того, при использовании асинхронного класса отличается использование сессии, поэтому перед выполнением методов необходимо вызывать асинхронный метод авторизации:

```python
my_station.authorize()
```
После выполнения всех необходимых методов необходимо вручную закрыть сессию:

```python
my_station.session.close()
```

Все управление колонкой осуществляется с помощью сценариев.
Вы можете получить дефолтные и добавленные сценарии с помощью метода:

```python
scenarios = my_station.get_scenarios()
```

Для добавления сценария используется метод:

```python
my_station.add_scenario(scenario_name='',
                        activation_command='',
                        instance='',
                        value='')
```

scenario_name - название сценария activation_command - голосовая команда для активации сценария в Алисе instance -
принимает значения:

'text_action' - для выполнения действия указанного в value

'phrase_action' - для озвучивания текста, указанного в value

value - действие или фраза в зависимости от типа instance

Для обновления сценария используется метод:

```python
my_station.update_scenatio(scenario_id='',
                           scenario_name='',
                           activation_command='',
                           instance='',
                           value='')
```
Для выполнения сценария используется метод:
```python
my_station.exec_scenario(scenario_id='')
```

Для удаления сценария используется метод:
```python
my_station.delete_scenario(scenario_id='')
```

