import requests
import json

res = requests.get('https://reqres.in/api/users?page=2')
print(json.dumps(res.json(), indent=2))
