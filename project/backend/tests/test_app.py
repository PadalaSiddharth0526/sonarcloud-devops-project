import pytest

from app import app, add, subtract, multiply, divide


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_calculate_add(client):
    response = client.post("/api/calculate", json={"operation": "add", "a": 2, "b": 3})
    assert response.status_code == 200
    assert response.get_json() == {"result": 5}


def test_calculate_subtract(client):
    response = client.post("/api/calculate", json={"operation": "subtract", "a": 5, "b": 3})
    assert response.status_code == 200
    assert response.get_json() == {"result": 2}


def test_calculate_multiply(client):
    response = client.post("/api/calculate", json={"operation": "multiply", "a": 4, "b": 3})
    assert response.status_code == 200
    assert response.get_json() == {"result": 12}


def test_calculate_divide(client):
    response = client.post("/api/calculate", json={"operation": "divide", "a": 10, "b": 2})
    assert response.status_code == 200
    assert response.get_json() == {"result": 5}


def test_calculate_divide_by_zero(client):
    response = client.post("/api/calculate", json={"operation": "divide", "a": 10, "b": 0})
    assert response.status_code == 400
    assert "Cannot divide by zero" in response.get_json()["error"]


def test_calculate_missing_fields(client):
    response = client.post("/api/calculate", json={"operation": "add", "a": 1})
    assert response.status_code == 400


def test_calculate_unsupported_operation(client):
    response = client.post("/api/calculate", json={"operation": "modulo", "a": 1, "b": 2})
    assert response.status_code == 400


def test_add_function():
    assert add(2, 3) == 5


def test_subtract_function():
    assert subtract(5, 3) == 2


def test_multiply_function():
    assert multiply(4, 3) == 12


def test_divide_function():
    assert divide(10, 2) == 5


def test_divide_function_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
