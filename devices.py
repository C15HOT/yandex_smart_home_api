import typing

from capabilities import OnOffCapability

if typing.TYPE_CHECKING:
    from api import YandexApi




class BaseDevice:
    def __init__(self, api: "YandexApi"):
        self.api = api

class Purifer(BaseDevice):
    async def info(self, device_id: str):
        info = await self.api.get_device_info(device_id=device_id)
        return info

    async def on_off(self, device_id: str, value: bool):
        return (await self.api.devices_action(device_id=device_id, actions=[OnOffCapability(type='on_off', value=value)()]))