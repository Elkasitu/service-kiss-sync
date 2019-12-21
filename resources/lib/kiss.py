import json
import requests


BASE_URL = 'http://localhost:5000/'


def fetch(hash):
    r = requests.get(BASE_URL + 'fetch/' + hash)
    assert r.ok, "Call to fetch endpoint failed, is the server running?"
    return json.loads(r.text)


def add(data):
    r = requests.post(BASE_URL + 'add', json=data)
    assert r.ok, "Call to add endpoint failed, is the server running?"
    return json.loads(r.text)


def update(data):
    r = requests.post(BASE_URL + 'update', json=data)
    assert r.ok, "Call to update endpoint failed, is the server running?"
    return json.loads(r.text)
