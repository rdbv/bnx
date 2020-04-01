from flask import Flask
import os, sys

sys.path[0] = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = os.urandom(16)

app.config['db_host'] = 'localhost'
app.config['db_user'] = 'data'
app.config['db_pass'] = '123456'
app.config['db_name'] = 'bnx'

app.config['photo_path'] = '/home/void/servers/bnx/photos/'

import bnx.views.index
import bnx.views.login
import bnx.views.logout
import bnx.views.error
import bnx.views.cam

