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


def test_user_invalid_characters(client):
    response = client.post(
        "/api/users",
        json={
            "username": "Juan@@@",
            "password": "password123"
        }
    )

    assert response.status_code == 422