import requests

print("Все пользователи сначала:",
      *[[el['name'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/v2/users').json().values()])

# добавить пользователя
data = {
    'surname': 'Kuertov',
    'name': 'Vladislav',
    'password': 'kuertovpassword',
    'password_again': 'kuertovpassword',
    'age': '21',
    'position': 'Boss',
    'speciality': 'Buisness-man',
    'address': 'secret',
    'email': 'majestic@mail.ru'
}

# добавление пользователя
print(requests.post('http://127.0.0.1:5000/api/v2/users', json=data).json())


print("Новый пользователь:", requests.get('http://127.0.0.1:5000/api/v2/users/10').json())

# эдит пользователя
data = {
    'surname': 'Kuertov',
    'name': 'Vladislavik',
    'password': 'kuertovpassword',
    'password_again': 'kuertovpassword',
    'age': '20',
    'position': 'Bossyara',
    'speciality': 'Mega Buisness-man',
    'address': 'Secret',
    'email': 'majesticboss@mail.ru'
}

# эдит пользователя
print(requests.put('http://127.0.0.1:5000/api/v2/users/10', json=data).json())

print("Все пользователи с изменённым новым:",
      *[[el['name'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/v2/users').json().values()])

# удаление пользователя
print(requests.delete('http://127.0.0.1:5000/api/v2/users/10').json())

print("Все пользователи в конце:",
      *[[el['name'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/v2/users').json().values()])

# неккоректный запрос на эдит
print(requests.put('http://127.0.0.1:5000/api/v2/users/10', json=data).json())

# неккоректный запрос на удаление
print(requests.delete('http://127.0.0.1:5000/api/v2/users/10').json())

# неккоректный запрос на получение пользователя
print(requests.get('http://127.0.0.1:5000/api/v2/users/машина').json())

# для неккоректного запроса эдит с неверным количеством полей
incorrect = {
    'surname': 'Kuertov',
    'name': 'Vladislavik',
    'password': 'kuertovpassword',
    'password_again': 'kuertovpassword',
    'age': '20',
    'position': 'Bossyara',
    'speciality': 'Mega Buisness-man',
}
print("Неверное количество полей в запросе:",
      requests.put('http://127.0.0.1:5000/api/v2/users/9', json=incorrect).json())