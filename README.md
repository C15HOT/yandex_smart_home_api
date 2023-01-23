# Yandex Smart Home API
### Что делает

Асинхронная библиотека для работы с Протоколом программного управления устройствами Яндекса.

### Установка зависимостей
```
pip install -r requirements.txt
```

## Как пользоваться

Необходимо создать экземпляр класса Yandex API, указав в атрибуте client_token токен, полученный по инструкции (https://yandex.ru/dev/dialogs/smart-home/doc/concepts/platform-protocol.html)

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

Для упрjщения работы реализован непосредственный доступ к устройствам путем создания 
экземпляра класса устройства, а также к доступным для устройств методам,
получению свойств, способностей и информации об устройстве.

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
