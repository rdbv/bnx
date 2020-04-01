from bnx import app

from bnx.utils.messages import Message
from bnx.database.db import Database

from flask import render_template, request, session, url_for, redirect

@app.route('/error', methods = ['GET'])
def error():
    return render_template('error.html')
