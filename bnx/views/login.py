from bnx import app

from bnx.utils.messages import Message
from bnx.database.db import Database

from flask import render_template, request, session, url_for, redirect, flash

@app.route('/login', methods = ['GET', 'POST'] )
def login():

    try:
        db = Database()
    except Exception as e:
        flash(e.message)
        return redirect(url_for('error'))

    if session.get('id') != None:
        return redirect(url_for('index'))

    message = Message()

    if request.method == 'POST':

        if request.form.get('login') == None or request.form.get('password') == None:
               return redirect(url_for('error'))

        user = db.getUser(**request.form)

        if user.id != None:
            session['id'] = 1
            return redirect(url_for('index'))
        else:
            message.addError('Niepoprawne dane')

    return render_template('login.html', messages = message)
