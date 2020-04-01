from bnx import app

from bnx.utils.messages import Message
from bnx.database.db import Database

from flask import render_template, request, session, url_for, redirect

@app.route('/', methods = ['GET'])
def index():

    if session.get('id') == None:
        return redirect(url_for('login'))

    return render_template('index.html')


