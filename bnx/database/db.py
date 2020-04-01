from bnx import app
from bnx.database.user import User

import MySQLdb as mdb

class DBError(Exception):

    def __init__(self, message):
        super().__init__()
        self.message = message

class Database:

    def __init__(self):

        self.con = None

        try:
            self.con = mdb.connect(app.config['db_host'],
                                   app.config['db_user'],
                                   app.config['db_pass'],
                                   app.config['db_name'],
                                   charset = 'utf8',
                                   use_unicode = True)
        except:
            raise DBError('Database connection error!')
        

    def __del__(self):

        if self.con:
            self.con.close()

    def getUser(self, login = None, password = None, id = None):
        cur = self.con.cursor()
    
        if id != None:
            cur.execute('SELECT * FROM users WHERE id="%s"' % (id))

        if login != None and password == None:
            cur.execute('SELECT * FROM users WHERE login = "%s"' % (login))

        if login != None and password != None:
            cur.execute('SELECT * FROM users WHERE login = "%s" AND password = "%s"' % (login, password))

        return User(cur.fetchone())

