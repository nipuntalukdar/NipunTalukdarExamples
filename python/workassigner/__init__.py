from flask import Flask, request, session, redirect, g, url_for,abort, \
    render_template, flash
import sqlite3

DATABASE = '/tmp/flask.db'
SECRET_KEY ='the key'
DEBUG = True
USERNAME = 'admin'
PASSWORD = 'admin'

def connect_db():
    return sqlite3.connect(DATABASE)

app = Flask('dataplot')
db = connect_db()
app.config.from_object(__name__)

@app.before_request
def before_request():
    print 'Before'
    g.db = db

@app.teardown_request
def teardown_request(exception):
    print 'Tear'

@app.after_request
def after_request(response):
    print 'After'
    return response

@app.route('/')
def route():
    return 'Hello'
if __name__ == '__main__':
    app.run(host='0.0.0.0')

