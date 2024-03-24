import requests

print("Все работы до изменения:",
      *[[el['job'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/jobs').json().values()])

# для корректного запроса
data = {
    'job_title': 'Archeologist',
    'team_leader': 6,
    'work_size': 30,
    'collaborators': '3, 4',
    'is_finished': False
}
# корректный запрос
print(requests.put('http://127.0.0.1:5000/api/jobs/edit_job/5', json=data).json())

print("Все работы после изменения:",
      *[[el['job'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/jobs').json().values()])

# неккоректный запрос: id работы больше максимального
print(requests.put('http://127.0.0.1:5000/api/jobs/edit_job/8', json=data).json())

# неккоректный запрос: id работы меньше минимального
print(requests.put('http://127.0.0.1:5000/api/jobs/edit_job/0', json=data).json())

# неккоректный запрос: id работы не является числом
print(requests.put('http://127.0.0.1:5000/api/jobs/edit_job/машина', json=data).json())

# для неккоректного запроса с неверным количеством полей
incorrect = {
    'job_title': 'Что угодно',
    'team_leader': 9,
    'work_size': 18,
    'is_finished': True,
}

# неверное количество полей
print("Неверное количество полей в запросе:",
      requests.put('http://127.0.0.1:5000/api/jobs/edit_job/1', json=incorrect).json())