from app import app
from flask import jsonify, render_template, abort, flash, redirect, url_for, request, g, make_response, session
from flask_login import login_user, logout_user, current_user, login_required
from .mock_data import users, lessons

@app.context_processor
def inject_lessons_count():
    return {'lesson_count': len(lessons)+1}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.j2')

@app.route('/get-started')
def getstarted():
    # 檢查用戶是否已登入
    if current_user.is_authenticated:
        return render_template('get-started.html.j2', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/how-it-works')
def howitworks():
    return render_template('how-it-works.html.j2')

@app.route('/login')
def login():
    return render_template('login.html.j2')

@app.route('/register')
def register():
    return render_template('register.html.j2')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html.j2')

@app.route('/lessonslist')
def get_lessonslist():
    return render_template('lessonslist.html.j2', lessons=lessons)

@app.route('/lesson/<int:lesson_id>')
def get_lesson(lesson_id):
    # Find the lesson by lesson_id
    lesson = next(
        (lesson for lesson in lessons if lesson['id'] == lesson_id), None)
    if lesson is None:
        abort(404)
    return render_template('lesson.html.j2', lesson_id=lesson_id, lesson_title=lesson['title'])
