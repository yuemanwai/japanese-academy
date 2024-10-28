from app import app
from flask import render_template, flash, redirect, url_for, request, g, make_response, session
from flask_login import login_user, logout_user, current_user, login_required

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
def register():
    return "需要做 register.html.j2"

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html.j2', title=_('Log out'))