import asyncio
import os
from pprint import pprint

import dotenv

from capabilities import OnOffCapability, Mode, Toggle
from api import YandexApi

from dotenv import load_dotenv


load_dotenv('.env')
token = dotenv.get_key(key_to_get='token', dotenv_path='.env')

api = YandexApi(client_token=token)


loop = asyncio.get_event_loop()

#
# pprint(loop.run_until_complete(api.get_device_info(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f')))


pprint(loop.run_until_complete(api.purifer.info(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f')))


# pprint(loop.run_until_complete(api.devices_action(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f',
#                                            actions=[OnOffCapability(type='on_off', value=False)()])))
#
#


# pprint(loop.run_until_complete(api.devices_action(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f',
#                                            actions=[OnOffCapability(type='on_off', value=True)()])))

# pprint(loop.run_until_complete(api.devices_action(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f',
#                                            actions=[Mode(type='mode', instance='work_speed', value='turbo')()])))

#
# pprint(loop.run_until_complete(api.devices_action(device_id='33954aba-713d-4193-8b1d-7d36f95bf51f',
#                                            actions=[Toggle(type='toggle', instance='pause', value=True)()])))

