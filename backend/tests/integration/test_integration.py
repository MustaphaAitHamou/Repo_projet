import json
import pytest
from app.routes import app, db

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as c:
        with app.app_context():
            # On vide la base avant la suite d’intégration
            db.drop_all()
            db.create_all()
        yield c

def test_full_flow(client):
    # CREATE
    resp1 = client.post(
        '/users',
        json={'email': 'int@egr.com', 'password': 'pw'}
    )
    assert resp1.status_code == 201
    data1 = json.loads(resp1.get_data())
    assert 'id' in data1

    # LIST
    resp2 = client.get('/users')
    assert resp2.status_code == 200
    users = json.loads(resp2.get_data())
    assert any(u['email'] == 'int@egr.com' for u in users)
