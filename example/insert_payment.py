import requests
from access_token import TOKEN

url = 'http://127.0.0.1:8000/api/payments/'

headers = {
    'Authorization': f'Bearer {TOKEN}',  # Use the token from get_token
    'Content-Type': 'application/json'
}


loan_id = 'baa968f4-890b-4dfd-bae0-7df398cd9daa'  # Replace with the actual loan ID
data = {
    'date': "2024-09-22T00:00:00Z",
    'value': 6000,
    'loan': loan_id
}

response = requests.post(url, json=data, headers=headers)

print(response.json())
