import requests

url = 'http://127.0.0.1:8000/api/token/'

data = {
    'username': 'testuser',
    'password': 'testpassword'
}

response = requests.post(url, data=data)

print(response.json())

token = response.json().get('access')
print("Access token:", token)
