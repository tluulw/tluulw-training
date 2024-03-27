import requests

print("Все работы сначала:",
      *[[el['job'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/v2/jobs').json().values()])

# добавить работу
data = {
    'job': 'cool new job',
    'team_leader': 8,
    'work_size': 45,
    'collaborators': '3, 6, 7',
    'is_finished': True
}

# добавление работы
print(requests.post('http://127.0.0.1:5000/api/v2/jobs', json=data).json())


print("Новая работа:", requests.get('http://127.0.0.1:5000/api/v2/jobs/7').json())

# эдит работы
data = {
    'job': 'cool edited new job',
    'team_leader': 7,
    'work_size': 45,
    'collaborators': '3, 6, 7, 8, 9',
    'is_finished': True
}

# эдит работы
print(requests.put('http://127.0.0.1:5000/api/v2/jobs/7', json=data).json())

print("Все работы с изменённой новой:",
      *[[el['job'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/v2/jobs').json().values()])

# удаление работы
print(requests.delete('http://127.0.0.1:5000/api/v2/jobs/7').json())

print("Все работы в конце:",
      *[[el['job'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/v2/jobs').json().values()])

# неккоректный запрос на эдит
print(requests.put('http://127.0.0.1:5000/api/v2/jobs/10', json=data).json())

# неккоректный запрос на удаление
print(requests.delete('http://127.0.0.1:5000/api/v2/jobs/10').json())

# неккоректный запрос на получение пользователя
print(requests.get('http://127.0.0.1:5000/api/v2/jobs/машина').json())