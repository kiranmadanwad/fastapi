from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == 200


def test_change_password(test_user):
    response = client.put("/user/password", json={"password": "testpassword", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_password(test_user):
    response = client.put("/user/password", json={"password": "testpassword1", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_phone_number(test_user):
    response = client.put("/user/phone_number/9999999999")
    assert response.status_code == status.HTTP_204_NO_CONTENT
