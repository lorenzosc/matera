import requests
from access_token import TOKEN

url = 'http://127.0.0.1:8000/api/loans/'

headers = {
    'Authorization': f'Bearer {TOKEN}',  # Use the token from get_token
    'Content-Type': 'application/json'
}

response = requests.get(url, headers=headers)

print(response.json())
