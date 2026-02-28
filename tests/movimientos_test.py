from app.models import Movimiento
import pytest
from app.models import User
from app.config.security import create_access_token

@pytest.fixture()
def test_user(db):
    user = User(username="Usuario Test", password="password123")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token(
        data={"sub": str(test_user.id)}
    )
    return {"Authorization": f"Bearer {access_token}"}

def test_create_movimiento_success(client, db, test_user, auth_headers):
    movimiento_response = client.post(
        f"/api/users/{test_user.id}/movimientos",
        json={
            "descripcion": "Compra de productos",
            "monto": 150.0,
            "tipo_movimiento": "gasto fijo",
            "categoria": "Supermercado",
            "cuenta_origen": "Tarjeta de crédito",
            "fecha": "2024-06-01"
        },
        headers=auth_headers
    )

    assert movimiento_response.status_code == 201
    movimiento_data = movimiento_response.json()

    assert movimiento_data["descripcion"] == "Compra de productos"
    assert movimiento_data["monto"] == 150.0
    assert movimiento_data["tipo_movimiento"] == "gasto fijo"
    assert movimiento_data["categoria"] == "Supermercado"
    assert movimiento_data["usuario_id"] == test_user.id
    assert movimiento_data["cuenta_origen"] == "Tarjeta de crédito"
    assert movimiento_data["fecha"] == "2024-06-01"

    # Verificar que se guardó en BD
    movimiento_in_db = db.query(Movimiento).filter(Movimiento.id == movimiento_data["id"]).first()
    assert movimiento_in_db is not None

def test_movimiento_validation_missing_field(client, test_user, auth_headers):
    response = client.post(
        f"/api/users/{test_user.id}/movimientos",
        json={
            "descripcion": "Compra de productos",
            "monto": 150.0,
            # Falta tipo_movimiento
            "categoria": "Supermercado",
            "cuenta_origen": "Tarjeta de crédito",
            "fecha": "2024-06-01"
        },
        headers=auth_headers
    )

    assert response.status_code == 422

    body = response.json()
    assert "detail" in body
    errors = body["detail"]
    tipo_movimiento_errors = [
        e for e in errors
        if e.get("loc") == ["body", "tipo_movimiento"] and "Field required" in e.get("msg", "")
    ]
    assert len(tipo_movimiento_errors) > 0

def test_movimiento_validation_extra_field(client, test_user, auth_headers):
    response = client.post(
        f"/api/users/{test_user.id}/movimientos",
        json={
            "descripcion": "Compra de productos",
            "monto": 150.0,
            "tipo_movimiento": "gasto fijo",
            "categoria": "Supermercado",
            "cuenta_origen": "Tarjeta de crédito",
            "fecha": "2024-06-01",
            "extra_field": "valor no permitido"  # campo no permitido
        },
        headers=auth_headers
    )

    assert response.status_code == 422

    body = response.json()
    assert "detail" in body
    errors = body["detail"]
    extra_field_errors = [
        e for e in errors
        if e.get("loc") == ["body", "extra_field"] and "Extra inputs are not permitted" in e.get("msg", "")
    ]
    assert len(extra_field_errors) > 0

def test_movimiento_invalid_characters(client, test_user, auth_headers):
    response = client.post(
        f"/api/users/{test_user.id}/movimientos",
        json={
            "descripcion": "Compra de productos<script>alert(1)</script>",
            "monto": 150.0,
            "tipo_movimiento": "gasto fijo",
            "categoria": "Supermercado",
            "cuenta_origen": "Tarjeta de crédito",
            "fecha": "2024-06-01"
        },
        headers=auth_headers
    )

    assert response.status_code == 422

    body = response.json()
    assert "detail" in body
    errors = body["detail"]
    descripcion_errors = [
        e for e in errors
        if e.get("loc") == ["body", "descripcion"] and "Caracteres no permitidos" in e.get("msg", "")
    ]
    assert len(descripcion_errors) > 0
    
def test_movimiento_invalid_tipo_movimiento(client, test_user, auth_headers):
    response = client.post(
        f"/api/users/{test_user.id}/movimientos",
        json={
            "descripcion": "Compra de productos",
            "monto": 150.0,
            "tipo_movimiento": "tipo inválido",  # valor no permitido
            "categoria": "Supermercado",
            "cuenta_origen": "Tarjeta de crédito",
            "fecha": "2024-06-01"
        },
        headers=auth_headers
    )

    assert response.status_code == 422

    body = response.json()
    assert "detail" in body
    errors = body["detail"]
    tipo_errors = [
        e for e in errors
        if e.get("loc") == ["body", "tipo_movimiento"] and "Tipo de movimiento inválido" in e.get("msg", "")
    ]
    assert len(tipo_errors) > 0
    