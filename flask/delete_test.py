import requests


print("Все работы до удаления:",
      *[[el['job'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/jobs').json().values()])

# удаление работы
print(requests.delete('http://127.0.0.1:5000/api/jobs/delete_job/7').json())

print("Все работы после удаления:",
      *[[el['job'] for el in elem] for elem in requests.get('http://127.0.0.1:5000/api/jobs').json().values()])



# неккоректный запрос: id работы больше максимального
print(requests.delete('http://127.0.0.1:5000/api/jobs/delete_job/7').json())

# неккоректный запрос: id работы меньше минимального
print(requests.delete('http://127.0.0.1:5000/api/jobs/delete_job/0').json())

# неккоректный запрос: id работы не является числом
print(requests.delete('http://127.0.0.1:5000/api/jobs/delete_job/машина').json())