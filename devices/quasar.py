import re

from pprint import pprint
from typing import Dict

import aiohttp
import requests

from asyncio import get_event_loop


class YandexSession:
    quasar_url = "https://iot.quasar.yandex.ru/m/user"
    music_url = "https://api.music.yandex.net"
    session = requests.session()
    csrf_token = None
    music_uid = 0
    login = ""
    password = ""

    def __init__(self, login, password, station_id):
        self.login = login
        self.password = password
        self.station_id = station_id
        self.session.headers.update({
            'User-Agent': 'Chrome',
            'Host': 'passport.yandex.ru'
        })

        resp = self.session.get("https://passport.yandex.ru/am?app_platform=android")
        m = re.search(r'"csrf_token" value="([^"]+)"', resp.text)
        auth_payload = {"csrf_token": m[1]}
        self.csrf_token = m[1]

        resp = self.session.post("https://passport.yandex.ru/registration-validations/auth/multi_step/start",
                                 {**auth_payload, "login": login}).json()

        auth_payload["track_id"] = resp["track_id"]

        self.session.post("https://passport.yandex.ru/registration-validations/auth/multi_step/commit_password",
                          {**auth_payload, "password": password,
                           'retpath': "https://passport.yandex.ru/am/finish?status=ok&from=Login"})

    def _update_csrf(self):
        raw = self.session.get("https://yandex.ru/quasar").text
        m = re.search('"csrfToken2":"(.+?)"', raw)
        self.csrf_token = m[1]

    def get_scenarios(self):
        return self.session.get(self.quasar_url + "/scenarios").json()['scenarios']

    def get_speakers(self):
        return self.session.get(self.quasar_url + "/devices").json()['speakers']

    def add_scenario(self, scenario_name: str, activation_command: str, instance: str, value: str):
        """
        instance: 'text_action' or 'phrase_action'
        """
        logic = {
            'type': 'devices.capabilities.quasar.server_action',
            'state': {
                'instance': instance,
                'value': value,
            }
        }
        payload = self.create_scenario(scenario_name=scenario_name, activation_command=activation_command, logic=logic)
        self._update_csrf()
        return self.session.post(self.quasar_url + "/scenarios", json=payload,
                                 headers={'x-csrf-token': self.csrf_token}).json()

    def update_scenario(self, scenario_id: str, scenario_name: str, activation_command: str, instance: str, value: str):
        logic = {
            'type': 'devices.capabilities.quasar.server_action',
            'state': {
                'instance': instance,
                'value': value,
            }
        }
        payload = self.create_scenario(scenario_name=scenario_name, activation_command=activation_command, logic=logic)
        self._update_csrf()
        self.session.put(self.quasar_url + "/scenarios/" + scenario_id, json=payload,
                         headers={'x-csrf-token': self.csrf_token})

    def delete_scenario(self, scenario_id):
        self._update_csrf()
        self.session.delete(self.quasar_url + "/scenarios/" + scenario_id,
                            headers={'x-csrf-token': self.csrf_token})

    def exec_scenario(self, scenario_id):
        self._update_csrf()
        return self.session.post(self.quasar_url + "/scenarios/" + scenario_id + "/actions",
                                 headers={'x-csrf-token': self.csrf_token}).json()

    def create_scenario(self, scenario_name: str, activation_command: str, logic: Dict):
        return {
            'name': scenario_name,
            'icon': 'home',
            'triggers': [{
                'type': 'scenario.trigger.voice',
                'value': activation_command
            }],
            'steps': [{
                'type': 'scenarios.steps.actions',
                'parameters': {
                    'requested_speaker_capabilities': [],
                    'launch_devices': [{
                        'id': self.station_id,
                        'capabilities': [logic]
                    }]
                }
            }]
        }




class YandexSessionAsync:
    quasar_url = "https://iot.quasar.yandex.ru/m/user"
    music_url = "https://api.music.yandex.net"
    session = aiohttp.ClientSession
    csrf_token = None
    music_uid = 0
    login = ""
    password = ""

    def __init__(self, login, password, station_id):
        self.login = login
        self.password = password
        self.station_id = station_id
        self.headers = {'User-Agent': 'Chrome',
                        'Host': 'passport.yandex.ru'
                        }
        self.session = self.session()

    async def authorize(self):
        response = await self.session.get(url="https://passport.yandex.ru/am?app_platform=android")
        resp = await response.text()
        m = re.search(r'"csrf_token" value="([^"]+)"', resp)

        auth_payload = {"csrf_token": m[1]}
        self.csrf_token = m[1]

        response = await self.session.post("https://passport.yandex.ru/registration-validations/auth/multi_step/start",
                                           data={'csrf_token': self.csrf_token, 'login': self.login}
                                           )
        resp = await response.json()
        auth_payload["track_id"] = resp["track_id"]

        await self.session.post(
            "https://passport.yandex.ru/registration-validations/auth/multi_step/commit_password",
            data={'csrf_token': self.csrf_token,
                  'track_id': auth_payload.get('track_id'),
                  'password': self.password,
                  'retpath': 'https://passport.yandex.ru/am/finish?status=ok&from=Login'})

    async def _update_csrf(self):
        response = await self.session.get("https://yandex.ru/quasar")
        raw = await response.text()
        m = re.search('"csrfToken2":"(.+?)"', raw)
        self.csrf_token = m[1]

    async def get_scenarios(self):
        response = await self.session.get(self.quasar_url + "/scenarios")
        resp = await response.json()
        scenarios = resp.get('scenarios')
        return scenarios

    async def get_speakers(self):
        response =  await self.session.get(self.quasar_url + "/devices")
        resp = await response.json()
        speakers = resp.get('speakers')
        return speakers

    async def add_scenario(self, scenario_name: str, activation_command: str, instance: str, value: str):
        """
        instance: 'text_action' or 'phrase_action'
        """
        logic = {
            'type': 'devices.capabilities.quasar.server_action',
            'state': {
                'instance': instance,
                'value': value,
            }
        }
        payload = await self.create_scenario(scenario_name=scenario_name, activation_command=activation_command, logic=logic)
        await self._update_csrf()
        response = await self.session.post(self.quasar_url + "/scenarios", json=payload,
                                 headers={'x-csrf-token': self.csrf_token})
        return await response.text()

    async def update_scenario(self, scenario_id: str, scenario_name: str, activation_command: str, instance: str, value: str):
        logic = {
            'type': 'devices.capabilities.quasar.server_action',
            'state': {
                'instance': instance,
                'value': value,
            }
        }
        payload = await self.create_scenario(scenario_name=scenario_name, activation_command=activation_command, logic=logic)
        await self._update_csrf()
        response = await self.session.put(self.quasar_url + "/scenarios/" + scenario_id, json=payload,
                         headers={'x-csrf-token': self.csrf_token})
        return await response.text()

    async def delete_scenario(self, scenario_id):
        await self._update_csrf()
        response = await self.session.delete(self.quasar_url + "/scenarios/" + scenario_id,
                            headers={'x-csrf-token': self.csrf_token})
        return await response.json()

    async def exec_scenario(self, scenario_id):
        await self._update_csrf()
        response = await self.session.post(self.quasar_url + "/scenarios/" + scenario_id + "/actions",
                                 headers={'x-csrf-token': self.csrf_token})
        return await response.json()

    async def create_scenario(self, scenario_name: str, activation_command: str, logic: Dict):
        return {
            'name': scenario_name,
            'icon': 'home',
            'triggers': [{
                'type': 'scenario.trigger.voice',
                'value': activation_command
            }],
            'steps': [{
                'type': 'scenarios.steps.actions',
                'parameters': {
                    'requested_speaker_capabilities': [],
                    'launch_devices': [{
                        'id': self.station_id,
                        'capabilities': [logic]
                    }]
                }
            }]
        }

#
# ys = YandexSessionAsync(login='leto2017a', password='gibsoncsv16xp', station_id='3e49a1b4-0700-4e50-a82d-0adf422cb58d')
#
# loop = get_event_loop()
# loop.run_until_complete(ys.authorize())
# pprint(loop.run_until_complete(ys.add_scenario(scenario_name='голос',
#                        activation_command='голос',
#                        instance='text_action',
#                        value='выключи очиститель воздуха')))
# scenarios = loop.run_until_complete(ys.get_scenarios())
# pprint(scenarios)
# scenario_id = [scenario['id'] for scenario in scenarios if scenario['name'] == 'голос'][0]
# pprint(loop.run_until_complete(ys.exec_scenario(scenario_id=scenario_id)))
# pprint(loop.run_until_complete(ys.delete_scenario(scenario_id=scenario_id)))
#
# #
# pprint(loop.run_until_complete(ys.update_scenario(scenario_id='11c5d1ff-1961-4530-9337-dbc74657d4c0', scenario_name='голос',
#                        activation_command='голос',
#                        instance='text_action',
#                        value='включи очиститель воздуха')))
# pprint(loop.run_until_complete(ys.exec_scenario(scenario_id='11c5d1ff-1961-4530-9337-dbc74657d4c0')))
# pprint(loop.run_until_complete(ys.delete_scenario(scenario_id='11c5d1ff-1961-4530-9337-dbc74657d4c0')))

# ys = YandexSession(login='leto2017a', password='gibsoncsv16xp', station_id='3e49a1b4-0700-4e50-a82d-0adf422cb58d')
#
# pprint(ys.add_scenario(scenario_name='голос',
#                        activation_command='голос',
#                        instance='text_action',
#                        value='выключи очиститель воздуха'))
# scenarios = ys.get_scenarios()
#
# scenario_id = [scenario['id'] for scenario in scenarios if scenario['name'] == 'голос'][0]
# pprint(scenarios)
#
# pprint(ys.exec_scenario(scenario_id=scenario_id))
#
# pprint(ys.delete_scenario(scenario_id=scenario_id))
#
