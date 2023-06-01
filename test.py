import requests
import json

url = 'http://localhost:8080'
payload = {'key': 'value'}
headers = {'Content-Type': 'application/json'}

response = requests.get(url, headers=headers)