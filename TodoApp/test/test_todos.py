from ..routers.todos import get_db, get_current_user
from fastapi import status
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'priority': '1', 'title': 'Test title', 'owner_id': 1, 'description': 'Test', 'id': 1,
                                'complete': False}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'priority': '1', 'title': 'Test title', 'owner_id': 1, 'description': 'Test', 'id': 1,
                               'complete': False}


def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}


def test_create_todo(test_todo):
    request_data = {
        'title': 'New Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.post('/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')


def test_update_todo(test_todo):
    request_data = {
        'title': 'Update Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todo/1', json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Update Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todo/2', json=request_data)
    assert response.status_code == 404


def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None



