import os
import pytest
from app import create_app
from flask import url_for


@pytest.fixture
def client():
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'TEST'
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Hello World ! Agile' in rv.data