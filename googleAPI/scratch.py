import requests
import json
from requests.exceptions import HTTPError

activityType = {
    'Сон': 72
}
sleepStages = {
    'Пробуждение (во время сна)': 1,
    'Спать': 2,
    'Из кровати': 3,
    'Легкий сон': 4,
    'Глубокий сон': 5,
    'РЭМ': 6
}

response = requests.get(
   'https://fitness.googleapis.com/fitness/v1/users/me/sessions',
    headers={'Authorization': 'Bearer ya29.a0AVvZVsqC-bZ1jmUzKXeuvY405C9pDj1FAt3lQkpIRbB4xmYSnQD-qKLjiFDwqRIteAPYCOXgIHK3Hl9qJbCIyr-ND7pcICj9-63DXXxN_UmN8FebHzcyL9UB9jmbBdHbFq45_uER6z6A1oIyD9P6eb5_0E9-6JYraCgYKAR8SAQASFQGbdwaI0dQo736tzHM0fvo7LIsH-g0167'}
)
response.encoding = 'utf-8'

#анализ ответа
print(response.status_code)
print(response.content)
print(response.text)
print(response.json())
print(response.url)
print(response.headers)


#анализ запроса
#print(response.request.headers['Content-Type'])
print(response.request.url)
print(response.request.path_url)
print(response.request.body)
print(response.request.headers)
print(response.request.method)

print("____________________________________________________________________________________________")
todos = json.loads(response.text)
print(todos)

#подсчет времени сна
for session in todos['session']:
    if session['activityType'] == activityType['Сон']:
        print(session)
        session['mytime'] = (int(session['endTimeMillis']) - int(session['startTimeMillis'])) / 1000 / 60 / 60
        #добавление к сессии сна все его фазы сна
        response2 = requests.post(
            url='https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate',
            json={
                "aggregateBy": [
                    {
                        "dataTypeName": "com.google.sleep.segment"
                    }
                ],
                "endTimeMillis": session['endTimeMillis'],
                "startTimeMillis": session['startTimeMillis']
            },
            headers={
                'Authorization': 'Bearer ya29.a0AVvZVsqC-bZ1jmUzKXeuvY405C9pDj1FAt3lQkpIRbB4xmYSnQD-qKLjiFDwqRIteAPYCOXgIHK3Hl9qJbCIyr-ND7pcICj9-63DXXxN_UmN8FebHzcyL9UB9jmbBdHbFq45_uER6z6A1oIyD9P6eb5_0E9-6JYraCgYKAR8SAQASFQGbdwaI0dQo736tzHM0fvo7LIsH-g0167'}
        )
        todos2 = json.loads(response2.text)
        print(todos2)
        session['mypoint'] = todos2['bucket'][0]['dataset'][0]['point']
print("____________________________________________________________________________________________")
print("результат - объединили сон + фазы сна")