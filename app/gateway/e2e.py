import requests
import random
import string


def random_string(length=8):
    return ''.join(random.sample(string.ascii_lowercase, length))


HOST = 'http://localhost:5000'
PREFIX = '/api/v1'

username = random_string()
password = random_string()

s = requests.Session()

r = s.post(f'{HOST}{PREFIX}/register', json={
    'username': username,
    'password': password,
})

assert r.status_code == 201

r = s.post(f'{HOST}{PREFIX}/login', json={
    'username': username,
    'password': password,
})
assert r.status_code == 200
assert r.json()['access_token'] != ''

print(r.json()['access_token'])
