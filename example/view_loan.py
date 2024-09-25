import requests
from access_token import TOKEN

loan_id = 'baa968f4-890b-4dfd-bae0-7df398cd9daa'  # Replace with the actual loan ID
url = f'http://127.0.0.1:8000/api/loans/{loan_id}/'

headers = {
    'Authorization': f'Bearer {TOKEN}',  # Use the token from get_token
    'Content-Type': 'application/json'
}

response = requests.get(url, headers=headers)

print(response.json())
