from app.models import User

def test_create_user_success(client, db):
    response = client.post(
        "/api/users",
        json={
            "username": "Juan",
            "password": "password123",
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["username"] == "Juan"

    # Verificar que se guardó en BD
    user_in_db = db.query(User).filter(User.username == "Juan").first()
    assert user_in_db is not None
    assert user_in_db.password != "password123"  # Verificar que la contraseña se haya hasheado

def test_user_validation_missing_field(client):
    response = client.post(
        "/api/users",
        json={
            "username": "Juan"
        }
    )

    assert response.status_code == 422

    body = response.json()
    assert "detail" in body
    errors = body["detail"]
    password_errors = [
        e for e in errors
        if e.get("loc") == ["body", "password"] and "Field required" in e.get("msg", "")
    ]
    assert len(password_errors) > 0

def test_user_validation_extra_field(client):
    response = client.post(
        "/api/users",
        json={
            "username": "Juan",
            "password": "password123",
            "age": 30  # campo no permitido
        }
    )

    assert response.status_code == 422

    body = response.json()
    assert "detail" in body
    errors = body["detail"]
    age_errors = [
        e for e in errors
        if e.get("loc") == ["body", "age"] and "Extra inputs are not permitted" in e.get("msg", "")
    ]
    assert len(age_errors) > 0


def test_user_invalid_characters(client):
    response = client.post(
        "/api/users",
        json={
            "username": "Juan@@@",
            "password": "password123"
        }
    )

    assert response.status_code == 422

    body = response.json()
    assert "detail" in body
    errors = body["detail"]
    descripcion_errors = [
        e for e in errors
        if e.get("loc") == ["body", "username"] and "Caracteres no permitidos" in e.get("msg", "")
    ]
    assert len(descripcion_errors) > 0