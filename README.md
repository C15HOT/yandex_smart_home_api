# Yandex Smart Home API
### Что делает

Библиотека для работы с Протоколом программного управления устройствами Яндекса.**

### Установка зависимостей
```
pip install -r requirements.txt
```

## Как пользоваться

Необходимо создать экземпляр класса Yandex API, указав в атрибуте client_token токен, полученный по инструкции (https://yandex.ru/dev/dialogs/smart-home/doc/concepts/platform-protocol.html)

```python
api = YandexApi(client_token=token)
```

Класс YandexApi позволяет напрямую обращаться к методам API, описанным в инструкции:

```python
api.get_device_info(device_id='')
```

Для упращения работы реализован непосредственный доступ к устройствам, а также к доступным для устройств методам,
получению свойств, способностей и информации об устройстве:

```python
api.purifer.info(device_id='')
api.purifer.on_off(device_id='', value=False)
api.vacuum_cleaner.get_capabilities(device_id='')
api.vacuum_cleaner.mode(device_id='', value='turbo')

```
