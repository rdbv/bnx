import pytest

import bnx

from bnx import app

from bnx.database.db import Database, DBError
from bnx.database.user import User

def test_db_connection():
    old_host = app.config['db_host']
    app.config['db_host'] = 'propably_bad_hostname'

    with pytest.raises(bnx.database.db.DBError):
        db = Database()

    app.config['db_host'] = old_host

def test_db_get_user():
    db = Database()
    
    user = db.getUser(id=1235123)
    assert user.id == None

    user = db.getUser(id=1)
    assert user.login == 'borbor'

    user = db.getUser(login='borbor')
    assert user.login == 'borbor'

    user = db.getUser(login='borbor', password='1')
    assert user.login == 'borbor'

    user = db.getUser(login='borbor', password='invalid_password')
    assert user.id == None



