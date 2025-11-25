from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_obtener_productos():
    response = client.get("/productos")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_crear_producto():
    nuevo_lacteo = {
        "id": 99,
        "nombre": "Queso Azul Test",
        "tipo": "Queso",
        "precio": 5.0,
        "stock": 10
    }
    response = client.post("/productos", json=nuevo_lacteo)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Queso Azul Test"