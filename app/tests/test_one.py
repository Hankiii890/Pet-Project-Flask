import pytest
from app.views import *
from main import db


@pytest.fixture()
def app_test():
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app_test):
    return app_test.test_client()


@pytest.fixture()
def runner(app_test):
    return app_test.test_cli_runner()


def test_index_view(client):
    response = client.get('/')
    assert response.status_code == 200


def test_cart_view(client):
    response = client.get('/cart')
    assert response.status_code == 200


def test_db_count():
    products = Medecine.query.all()
    assert len(products) == 5
