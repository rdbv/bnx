from bnx import app

from bnx.utils.messages import Message
from bnx.database.db import Database

from flask import render_template, request, session, url_for, redirect

@app.route('/logout', methods = ['GET'])
def logout():

    session.pop('id',None)
    return redirect(url_for('index'))
