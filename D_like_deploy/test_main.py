from fastapi.testclient import TestClient
import pytest
from D_like_deploy.main import app

client = TestClient(app)
counter = 0


# exercises from lecture number 1
@pytest.mark.parametrize("name", ['Zenek', 'Marek', 'Alojzy Niezdąży'])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {'msg': f"Hello {name}"}


def test_receive_something():
    response = client.post("/dej/mi/coś", json={'first_key': 'some_value'})
    assert response.json() == {"received": {'first_key': 'some_value'},
                               "constant_data": "python jest super"}
# end of exercises from lecture number 1


# homework from lecture number 1
def test_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}


def test_method_name():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET" or "POST" or "DELETE" or "PUT"}
# end of homework from lecture number 1
