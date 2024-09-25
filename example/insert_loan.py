import requests
from access_token import TOKEN

url = 'http://127.0.0.1:8000/api/loans/'

headers = {
    'Authorization': f'Bearer {TOKEN}',  # Use the token from get token
    'Content-Type': 'application/json'
}

data = {
    'value': 1200,
    'interest_rate': 10,
    'request_date': "2024-05-30T00:00:00Z",
    'ip_address': "192.168.0.3",
    'bank': "Test Bank",
    'client': "John Doe"
}

response = requests.post(url, json=data, headers=headers)

print(response.json())
