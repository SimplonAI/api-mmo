import os
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SERVER_NAME": "exemple.com",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test"
    })

    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    yield client

def test_index_nologin(client):
    """Test for the index page
    """
    rv = client.get('/')
    assert rv.status_code == 302