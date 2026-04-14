from http.client import responses

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..routers.auth import get_current_user
from fastapi.testclient import TestClient
import pytest



from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db]= override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_return_user(test_user):
    response= client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ['username'] == 'labanya'
    assert response.json()['email'] == 'labanyaroy1488@gmail.com'
    assert response.json()['first_name'] == 'Labanya'
    assert response.json() ['last_name'] == 'roy'
    assert response.json() ['role'] == 'admin'
    assert response.json()['phone_number'] == '8967418564'

def test_change_password_success(test_user):
    response= client.put("/user/password", json ={"password":"testpassword","new_password":"new_password"})
    assert response.status_code ==status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={"password": "wrong_password", "new_password": "new_password"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()=={'detail':'Error on password'}


def test_change_phone_number_success(test_user):
    response =client.put("/user/phonenumber/8967543456")
    assert response.status_code==status.HTTP_204_NO_CONTENT










