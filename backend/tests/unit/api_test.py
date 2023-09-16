import pytest
from backend.src.app import create_app


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        yield testing_client


def test_home_page_with_fixture(test_client):
    """ """
    response = test_client.post("/chatgpt")
    assert response.status_code == 200
