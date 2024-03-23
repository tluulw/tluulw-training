import requests

# все работы до добавления
print("Работы до добавления новой:",
      *[[el['job'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/jobs').json().values()])

# json, содержащий данные для добавления работы
data = {
    'job_title': 'Drainer',
    'team_leader': 9,
    'work_size': 18,
    'collaborators': '6, 7',
    'is_finished': True
}

# добавление новой работы
requests.post('http://127.0.0.1:5000/api/jobs/add_job', json=data)

# все работы после добавления новой
print("Работы после добавления новой:",
      *[[el['job'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/jobs').json().values()])

# для неккоректного запроса с одним отсутствующим полем
incorrect_1 = {
    'job_title': 'Что угодно',
    'team_leader': 9,
    'work_size': 18,
    'is_finished': True,
}

# одно отсутствующее поле
print("Отсутствует поле:", requests.post('http://127.0.0.1:5000/api/jobs/add_job', json=incorrect_1).text)

# для неккоректного запроса с одним лишним полем
incorrect_2 = {
    'job_title': 'Что угодно',
    'team_leader': 9,
    'work_size': 18,
    'is_finished': True,
}

# одно лишнее поле
print("Лишнее поле:", requests.post('http://127.0.0.1:5000/api/jobs/add_job', json=incorrect_2).text)

# для неккоректного запроса с существующим названием работы
incorrect_3 = {
    'job_title': 'Sportsman',
    'team_leader': 2,
    'work_size': 3,
    'collaborators': '1, 2',
    'is_finished': False
}

# работа существует
print(requests.post('http://127.0.0.1:5000/api/jobs/add_job', json=incorrect_3).text)