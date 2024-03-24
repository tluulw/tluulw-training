import requests

print(requests.delete('http://127.0.0.1:5000/api/jobs/delete_job/7').json())