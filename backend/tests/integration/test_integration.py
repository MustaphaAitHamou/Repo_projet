# tests/integration/test_integration.py

import pytest
from app.routes import app, db

@pytest.fixture(scope="module")
def client():
    # Passe l'app en mode testing et bascule en SQLite en mémoire
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Crée les tables avant le premier test
    with app.app_context():
        db.create_all()

    # Fournit un test client
    with app.test_client() as client:
        yield client

def test_full_flow(client):
    # 1) Création d'un utilisateur
    response = client.post(
        '/users',
        json={'email': 'test@example.com', 'password': 'secret'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data

    # 2) Vérification que l'utilisateur apparaît dans la liste
    response = client.get('/users')
    assert response.status_code == 200
    users = response.get_json()
    assert any(user['email'] == 'test@example.com' for user in users)
