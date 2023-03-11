
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from waitress import serve
from datetime import datetime
from flask import send_from_directory
import os
import html
import re
import sqlite3



app=Flask(__name__)


@app.route('/')
def inicio():
    
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def imagen(imagen):
    return send_from_directory(os.path.join('templates/sitio/img'), imagen)

@app.route("/css/<css>")
def css_link(css):
    return send_from_directory(os.path.join('templates/sitio/css'), css)
@app.route("/js/<js>")
def js_link(js):
    return send_from_directory(os.path.join('templates/sitio/js'), js)
@app.route("/fonts/<fonts>")
def fonts_link(fonts):
    return send_from_directory(os.path.join('templates/sitio/fonts'), fonts)

@app.route('/about')
def about():
    return render_template('sitio/about.html')

@app.route('/mangas')
def manga():
    return render_template('sitio/Mangas.html')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)