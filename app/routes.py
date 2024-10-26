from app import app
from flask import render_template

@app.route('/')
def home():
    return render_template('index.html.j2')

@app.route('/get-started')
def getstarted():
    return render_template('get-started.html.j2')

@app.route('/get-started')
def howitworks():
    return render_template('how-it-works.html.j2')

@app.route('/login')
def login():
    return "未做好"