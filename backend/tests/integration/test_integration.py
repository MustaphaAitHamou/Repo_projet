# backend/tests/integration/test_integration.py

import pytest
import json
from app.routes import app, db

@pytest.fixture(scope="module")
def client():
    # passe l'app en mode testing et bascule en SQLite en mémoire
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # créer les tables avant le premier test
    with app.app_context():
        db.create_all()

    # fournir le test_client
    with app.test_client() as c:
        yield c

def test_full_flow(client):
    # 1) Création d’un utilisateur
    rv1 = client.post(
        '/users',
        json={'email': 'int@egr.com', 'password': 'pw'}
    )
    assert rv1.status_code == 201
    data1 = rv1.get_json()
    assert 'id' in data1

    # 2) Lecture de la liste
    rv2 = client.get('/users')
    assert rv2.status_code == 200
    users = rv2.get_json()
    # on vérifie que notre utilisateur est bien dans la liste
    assert any(u['email'] == 'int@egr.com' for u in users)
