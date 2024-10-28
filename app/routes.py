from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html.j2')

@app.route('/get-started')
def getstarted():
    return render_template('get-started.html.j2')

@app.route('/how-it-works')
def howitworks():
    return "需要做 how-it-works.html.j2"

@app.route('/login')
def login():
    return "需要做 login.html.j2"

@app.route('/register')
def login():
    return "需要做 register.html.j2"