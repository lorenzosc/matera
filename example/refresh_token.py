import requests

refresh_url = 'http://127.0.0.1:8000/api/token/refresh/'

refresh_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNzMyNDAwMSwiaWF0IjoxNzI3MjM3NjAxLCJqdGkiOiIyMGZkMGE4YmVlZmU0ZWRiOTFjNGYwZDhkZTQ1YmFhMyIsInVzZXJfaWQiOjF9.FPxjBX13KgV5BCoPfpAAK70uLMfSDpkaacgJmDMIpMA'

data = {
    'refresh': refresh_token
}

response = requests.post(refresh_url, data=data)

new_access_token = response.json().get('access')
print("New Access Token:", new_access_token)

with open('example/access_token.py', 'w') as f:
    f.write('# Insert token here\n')
    f.write(f'TOKEN = "{new_access_token}"\n')
