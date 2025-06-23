import pytest
import json
from app.routes import app, db
from app.models import User

@pytest.fixture
def client(monkeypatch):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as c:
        with app.app_context():
            # On vide la base avant chaque test unitaire
            db.drop_all()
            db.create_all()
        yield c

def test_add_list_user(client):
    # POST
    rv = client.post('/users', json={'email': 'a@b.c', 'password': 'p'})
    assert rv.status_code == 201
    data = json.loads(rv.data)
    assert 'id' in data

    # GET list
    rv2 = client.get('/users')
    assert rv2.status_code == 200
    users = json.loads(rv2.data)
    assert any(u['email'] == 'a@b.c' for u in users)
