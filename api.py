import json
from abc import ABC, abstractmethod
from pprint import pprint
from typing import Dict, List
import typing
import aiohttp
import asyncio

token = 'y0_AgAAAAAfll3JAAkELQAAAADaD3TazEaEAM3GSi61hOmlMrrA_VmQV2Y'

if typing.TYPE_CHECKING:
    from devices import BaseDevice

from devices import Purifer

class DeviceCategories(ABC):
    @property
    def purifer(self):
        return Purifer(self.api_instance)

    @property
    @abstractmethod
    def api_instance(self) -> "YandexApi":
        pass


class ABCAPI(DeviceCategories, ABC):
    @property
    def api_instance(self) -> "ABCAPI":
        return self


class YandexApi(ABCAPI):

    def __init__(self, client_token,
                 host='https://api.iot.yandex.net',
                 version='/v1.0'):
        self.client_token = client_token
        self.host = host
        self.headers = {'Authorization': "Bearer {}".format(token)}
        self.version = version

    async def get_smart_home_info(self, resource='/user/info') -> Dict:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f'{self.host}{self.version}{resource}') as response:
                result = await response.json()
                return result

    async def get_device_info(self, device_id, resource='/devices/') -> Dict:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f'{self.host}{self.version}{resource}{device_id}') as response:
                result = await response.json()
                return result

    async def get_group_info(self, group_id, resource='/groups/') -> Dict:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f'{self.host}{self.version}{resource}{group_id}') as response:
                result = await response.json()
                return result

    async def delete_device(self, device_id, resource='/devices/') -> Dict:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.delete(f'{self.host}{self.version}{resource}{device_id}') as response:
                result = await response.json()
                return result


    async def devices_action(self, device_id, actions: List[Dict], resource='/devices/actions') -> Dict:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            data = {
                    'devices': [{
                        'id': f'{device_id}',
                        'actions': actions
                    }]
                }

            async with session.post(f'{self.host}{self.version}{resource}',
                                    data=json.dumps(data)) as response:
                result = await response.json()
                return result

    async def group_action(self, group_id, data: Dict, resource='/groups/'):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(f'{self.host}{self.version}{resource}{group_id}/actions',
                                    data=json.dumps(data)) as response:
                result = await response.json()
                return result

    async def scenario_action(self, scenario_id, resource='/scenarios/'):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(f'{self.host}{self.version}{resource}{scenario_id}/actions') as response:
                result = await response.json()
                return result

#
# q = YandexApi(client_token=token)

# loop = asyncio.get_event_loop()
# pprint(loop.run_until_complete(q.get_smart_home_info()))
# print('\n')
# pprint(loop.run_until_complete((q.delete_device(device_id='8481f9ef-cb6d-47d4-9ae9-e1f759000a3b'))))
