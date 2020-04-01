from bnx import app
from flask import render_template, request, session
import os

@app.route('/cam', methods = ['GET'] )
def cam():
        
    paths = []
    for photo in os.listdir(app.config['photo_path']):
        paths.append('../photos/'+photo)

    return render_template('cam.html', photos = paths)
