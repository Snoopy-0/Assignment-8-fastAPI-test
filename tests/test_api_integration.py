from fastapi.testclient import TestClient
from main import app   

client = TestClient(app)

def call(op, a, b):
    return client.post(f"/{op}", json={"a": a, "b": b})

def test_add_endpoint():
    r = call("add", 2, 3)
    assert r.status_code == 200
    assert r.json()["result"] == 5

def test_subtract_endpoint():
    r = call("subtract", 5, 2)
    assert r.status_code == 200
    assert r.json()["result"] == 3

def test_multiply_endpoint():
    r = call("multiply", 3, 4)
    assert r.status_code == 200
    assert r.json()["result"] == 12

def test_divide_endpoint_ok():
    r = call("divide", 10, 2)
    assert r.status_code == 200
    assert r.json()["result"] == 5

def test_divide_endpoint_by_zero():
    r = call("divide", 1, 0)
    assert r.status_code == 400
    assert "Division by zero" in r.json()["detail"]

def test_validation_error():
    r = call("add", "x", 2)
    assert r.status_code == 422
