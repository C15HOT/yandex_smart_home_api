from pprint import pprint

import aiohttp
import asyncio
import time
import json

client_id = '9870ff5eb75d44318b3b226c1a4fa21a'
# device_id=<идентификатор устройства
# device_name=<имя устройства>]
redirect_uri = 'https://oauth.yandex.ru/verification_code'
login_hint = 'leto2017a'
# scope=<запрашиваемые необходимые права>]
# optional_scope=<запрашиваемые опциональные права>]
# force_confirm=yes]
# state=<произвольная строка>]

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By


class DzenParser:
    def __init__(self, password):
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-infobars')
        # self.chrome_options.add_argument('--remote-debugging-port=9222')
        # self.chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(options=self.chrome_options)

        self.password = password
        self.link = f'https://oauth.yandex.ru/authorize?response_type=token&client_id={client_id}&redirect_uri={redirect_uri}&login_hint={login_hint}'

    def authorization(self):
        """
        Авторизация в Дзене
        :return:
        """
        self.driver.get(self.link)

        mail = self.driver.find_element(By.XPATH,
                                        '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[1]/div[1]/button').click()
        login = self.driver.find_element(By.XPATH,
                                         '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[2]/div/div[2]/span/input')
        time.sleep(3)

        login_enter = self.driver.find_element(By.CSS_SELECTOR, '#passp\:sign-in')
        login_enter.click()
        time.sleep(3)
        password = self.driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/form/div[2]/div[1]/span/input')
        password.send_keys(self.password)
        password_enter = self.driver.find_element(By.CSS_SELECTOR, '#passp\:sign-in')
        password_enter.click()
        time.sleep(3)
        try:
            button = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[2]/form/div[1]/button').click()
            time.sleep(3)
        except:
            pass
        token = self.driver.find_element(By.CLASS_NAME, 'verification-code-flow-token-output')
        token = token.text
        return token


async def main():
    token = 'y0_AgAAAAAfll3JAAkELQAAAADaD3TazEaEAM3GSi61hOmlMrrA_VmQV2Y'
    headers = {'Authorization': "Bearer {}".format(token)}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://api.iot.yandex.net/v1.0/user/info') as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.json()
            pprint(html)
    print('\n')

    device_id = '8481f9ef-cb6d-47d4-9ae9-e1f759000a3b'

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://api.iot.yandex.net/v1.0/devices/{device_id}') as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.json()
            pprint(html)

    print('\n')

    # async with aiohttp.ClientSession(headers=headers) as session:
    #     data = {
    #         'devices': [{
    #             'id': '8481f9ef-cb6d-47d4-9ae9-e1f759000a3b',
    #             'actions': [{
    #                 'type': 'devices.capabilities.on_off',
    #                 'state': {'instance': 'on',
    #                           'value': False}
    #             }]
    #         }]
    #     }
    #
    #     async with session.post(f'https://api.iot.yandex.net/v1.0/devices/actions',
    #                             data=json.dumps(data)) as response:
    #         print("Status:", response.status)
    #         print("Content-type:", response.headers['content-type'])
    #
    #         html = await response.json()
    #         pprint(html)


# yandex = DzenParser(password='gibsoncsv16xp')
# token = yandex.authorization()
# print(token)
# #
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
