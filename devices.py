import typing

from capabilities import OnOff, Mode, Toggle

if typing.TYPE_CHECKING:
    from api import YandexApi


class BaseDevice:
    def __init__(self, api: "YandexApi"):
        self.api = api

    async def info(self, device_id: str):
        info = await self.api.get_device_info(device_id=device_id)
        return info

    async def get_properties(self, device_id: str):
        info = await self.api.get_device_info(device_id=device_id)
        properties = info.get('properties')
        return properties

    async def get_capabilities(self, device_id: str):
        info = await self.api.get_device_info(device_id=device_id)
        properties = info.get('capabilities')
        return properties


class Purifer(BaseDevice):

    async def on_off(self, device_id: str, value: bool):
        return (await self.api.devices_action(device_id=device_id, actions=[OnOff(type='on_off', value=value)()]))


class VacuumCleaner(BaseDevice):

    async def on_off(self, device_id: str, value: bool):
        return (await self.api.devices_action(device_id=device_id, actions=[OnOff(type='on_off', value=value)()]))

    async def mode(self, device_id: str, value: str):
        return (await self.api.devices_action(device_id=device_id, actions=[Mode(type='mode', value=value)()]))

    async def toggle(self, device_id: str, value: bool):
        return (await self.api.devices_action(device_id=device_id, actions=[Toggle(type='toggle', value=value)()]))
