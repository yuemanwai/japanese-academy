import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

@allure.step("Test index route")
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

@allure.step("Test home route")
def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200

@allure.step("Test login GET route")
def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Sign in' in response.data or b'login' in response.data.lower()

@allure.step("Test register GET route")
def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Sign up' in response.data or b'register' in response.data.lower()

@allure.step("Test logout route")
def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 200

@allure.step("Test comingsoon route")
def test_comingsoon(client):
    response = client.get('/comingsoon')
    assert response.status_code == 200

@allure.step("Test lessons_list route")
def test_lessons_list(client):
    response = client.get('/lessons_list')
    assert response.status_code == 200

@allure.step("Test practice route")
def test_practice(client):
    response = client.get('/practice')
    assert response.status_code == 200

@allure.step("Test dictionary route")
def test_dictionary(client):
    response = client.get('/dictionary')
    assert response.status_code == 200

@allure.step("Test community route")
def test_community(client):
    response = client.get('/community')
    assert response.status_code == 200

@allure.step("Test chat_with_copilot GET route")
def test_chat_with_copilot_get(client):
    response = client.get('/chat_with_copilot')
    assert response.status_code == 200

@allure.step("Test leave_message GET route")
def test_leave_message_get(client):
    response = client.get('/leave_message')
    assert response.status_code == 200

@allure.step("Test donate GET route")
def test_donate_get(client):
    response = client.get('/donate')
    assert response.status_code == 200

@allure.step("Test search GET route")
def test_search_get(client):
    response = client.get('/search')
    assert response.status_code == 200

@allure.step("Test login POST with invalid credentials")
def test_login_post_invalid(client):
    response = client.post('/login', data={'username': 'invalid', 'password': 'invalid'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data or b'Sign in' in response.data

# ...existing code...
