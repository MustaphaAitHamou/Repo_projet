import requests
import pytest

def test_full_flow():
    # Assure que docker-compose est up
    base = 'http://localhost:5000'
    # Ajouter
    r1 = requests.post(f'{base}/users', json={'email':'int@egr.com','password':'pw'})
    assert r1.status_code == 201
    uid = r1.json()['id']
    # Lister
    r2 = requests.get(f'{base}/users')
    assert any(u['id']==uid for u in r2.json())
    # Supprimer (admin)
    r3 = requests.delete(f'{base}/users/{uid}', headers={'X-Admin-Token':'PvdrTAzTeR247sDnAZBr'})
    assert r3.status_code == 204