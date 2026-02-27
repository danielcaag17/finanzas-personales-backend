from app.models import User

def test_create_user_success(client, db):
    response = client.post(
        "/api/users",
        json={
            "name": "Juan",
            "email": "juan123@example.com",
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Juan"
    assert data["email"] == "juan123@example.com"

    # Verificar que se guardó en BD
    user_in_db = db.query(User).filter(User.name == "Juan").first()
    assert user_in_db is not None

def test_user_validation_missing_field(client):
    response = client.post(
        "/api/users",
        json={
            "name": "Juan"
        }
    )

    assert response.status_code == 422

def test_user_validation_extra_field(client):
    response = client.post(
        "/api/users",
        json={
            "name": "Juan",
            "email": "juan123@example.com",
            "age": 30  # campo no permitido
        }
    )

    assert response.status_code == 422


def test_user_invalid_characters(client):
    response = client.post(
        "/api/users",
        json={
            "name": "Juan@@@",
            "username": "juan###"
        }
    )

    assert response.status_code == 422