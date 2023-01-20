import asyncio
from pprint import pprint

from capabilities import OnOffCapability, Mode, Toggle
from api import YandexApi

token = 'y0_AgAAAAAfll3JAAkELQAAAADaD3TazEaEAM3GSi61hOmlMrrA_VmQV2Y'

api = YandexApi(client_token=token)

loop = asyncio.get_event_loop()

#
# pprint(loop.run_until_complete(api.get_device_info(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f')))


pprint(loop.run_until_complete(api.puriffer.info(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f')))


pprint(loop.run_until_complete(api.devices_action(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f',
                                           actions=[OnOffCapability(type='on_off', value=False)()])))




# pprint(loop.run_until_complete(api.devices_action(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f',
#                                            actions=[OnOffCapability(type='on_off', value=True)()])))

# pprint(loop.run_until_complete(api.devices_action(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f',
#                                            actions=[Mode(type='mode', instance='work_speed', value='turbo')()])))

#
# pprint(loop.run_until_complete(api.devices_action(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f',
#                                            actions=[Toggle(type='toggle', instance='pause', value=True)()])))

