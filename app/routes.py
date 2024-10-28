from app import app
from flask import render_template, abort, flash, redirect, url_for, request, g, make_response, session
from flask_login import login_user, logout_user, current_user, login_required

# Mock lessons data
lessons = [
    {'id': 1, 'title': 'Mastering Hiragana and Katakana'},
    {'id': 2, 'title': 'Handwriting Practice'},
    {'id': 3, 'title': 'Grammar Essentials'},
]

@app.context_processor
def inject_lessons_count():
    return {'lesson_count': len(lessons)+1}

@app.route('/')
@app.route('/index')
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
    return render_template('logout.html.j2')


@app.route('/lessonslist')
def lessonslist():
    return render_template('lessonslist.html.j2')

@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    # Find the lesson by lesson_id
    lesson = next(
        (lesson for lesson in lessons if lesson['id'] == lesson_id), None)
    if lesson is None:
        abort(404)
    return render_template('lesson.html.j2', lesson_id=lesson_id, lesson_title=lesson['title'])
