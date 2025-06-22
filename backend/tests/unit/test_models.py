import pytest
from app.models import User

@pytest.fixture
def user():
    u = User(email='test@example.com')
    u.set_password('secret')
    return u

def test_password_hashing(user):
    assert user.check_password('secret')
    assert not user.check_password('wrong')