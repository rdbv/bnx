import os
import tempfile
import pytest

from bnx import app

def test_login_redirect():
    response = app.test_client().get('/')
    assert response.status_code == 302

def test_login_invalid_post_headers():
    response = app.test_client().post('/login', data=dict(
            some_text ='borbor'
        ), follow_redirects = True)

    assert response.status_code == 200
    assert b'Error' in response.data

def test_login_valid_post_headers():
    response = app.test_client().post('/login', data=dict(
        login='borbor', 
        password='1',
        ), follow_redirects = True)
    
    assert response.status_code == 200
    assert response.headers.get('id') == 1
        

