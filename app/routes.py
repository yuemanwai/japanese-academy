from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, g, make_response, session, jsonify, current_app, Response
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from flask_babel import _, get_locale, refresh
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, DonationForm, PaymentForm, LeaveMessageForm, SearchForm
from app.models import User, Post, Image, Donor, Payment, IP, Leave_message, Lesson, Level, ChatSettings,Evaluation
from app.email_service import send_password_reset_email
import os
import time
import random 
import subprocess
from app.copilot import CopilotChat
from werkzeug.utils import secure_filename
from mimetypes import guess_type
from app.gemini import GeminiClient  
from urllib.parse import quote
import json
import re  
import matplotlib.pyplot as plt
import numpy as np
import io
import base64


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())
    g.search_form = SearchForm()  # 初始化 SearchForm


@app.context_processor
def inject_lessons_count():
    return {'site_name': 'JP Academy'}

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html.j2')

# 一D未做好的頁面都set跳去呢度, 盡量唔爆error
@app.route('/comingsoon', methods=['GET'])
def shared():
    return render_template('shared.html.j2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data,
                   duration=timedelta(days=365))
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html.j2', title=_('Sign in'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html.j2', title=_('Sign out'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are one of us now!'))
        return redirect(url_for('index'))
    return render_template('register.html.j2', title=_('Sign up'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        # Add a random delay
        time.sleep(random.randint(1, 5))  # Use the correct random module
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html.j2',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html.j2', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def user():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(
            title=current_user.username).first() or None
        if not post:
            post = Post(title=current_user.username, body=form.body.data)
            db.session.add(post)
            ip = IP.query.filter_by(post_id=post.id).first() or None
            if not ip:
                ip = IP(post_id=post.id, ip_addr=request.remote_addr)
                db.session.add(ip)
                flash('We will store your IP address')
        else:
            if form.title.data != current_user.username:
                flash('Cannot change user page title.')
                return redirect(url_for('user', username=current_user.username))
            post.body = form.body.data
            image = Image.query.filter_by(post_id=post.id).first() or None
            if image:
                image.post_id = post.id
                image.filename = post.title
            f = form.image.data
            filename = secure_filename(post.title)
            f.save(os.path.join(
                "app", 'static', 'image', filename)+'.jpg')
            image = Image(post_id=post.id, filename=post.title)
            db.session.add(image)
        db.session.commit()
        flash(_('Your user page has been saved.'))
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        post = Post.query.filter_by(
            title=current_user.username).first() or None
        if post:
            form.title.data = post.title
            form.body.data = post.body
    image_path = os.path.join('static', 'image', user.username)+'.jpg'
    return render_template('profile.html.j2',  title=_(f'Hello, {current_user.username.capitalize()}!'), form=form, user=user, image_path=image_path)


@app.route('/edit', methods=['GET', 'POST'])
def edit(): 
    title = request.args.get('title')
    if title is None:
        print("No title provided")
    post = Post.query.filter_by(title=title).first()
    form = EditForm(edit_post=post.body)
    if form.validate_on_submit():
        if form.submit.data:
            post.body = form.edit_post.data
            db.session.commit()
            flash(_('Changes have been saved.'))
        elif form.cancel.data:
            flash(_('Changes have been canceled.'))
        return redirect(url_for('wiki', title=title))
    elif request.method == 'GET':
        form.edit_post.data = post.body
    return render_template('edit.html.j2', title=_(f'Editing {post.title}'), form=form)


@app.route('/follow/<title>', methods=['POST'])
@login_required
def follow(title):
    post = Post.query.filter_by(title=title).first()
    current_user.follow(post)
    db.session.commit()
    following_article = True
    flash(_('<%(title)s> and its talk page have been added to your watchlist permanently.', title=title))
    return redirect(url_for('wiki', title=title, following_article=following_article))


@app.route('/unfollow/<title>', methods=['POST'])
@login_required
def unfollow(title):
    post = Post.query.filter_by(title=title).first()
    current_user.unfollow(post)
    db.session.commit()
    following_article = False
    flash(_('<%(title)s> and its talk page have been removed from your watchlist.', title=title))
    return redirect(url_for('wiki', title=title, following_article=following_article))


@app.route('/Watchlist/<username>')
@login_required
def watchlist(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.followed_posts().all()
    count = user.followed_posts().count()
    return render_template('watchlist.html.j2', title=_('Watchlist'), posts=posts, count=count)


@app.route('/random_post')
def get_random_post():
    posts = Post.query.all()
    if not posts:
        return render_template('random_post.html.j2', title=None)
    
    post = random.choice(posts)
    user = post.user if post.user_id else None
    return render_template('random_post.html.j2', title=post.title, posts=[post], user=user)


@app.route('/randompost/<title>')
def random_post(title):
    post = Post.query.filter_by(title=title).first()
    if post:
        if current_user.is_authenticated:
            following_post = current_user.is_following(post)
            return render_template('random_post.html.j2', category=_('Article'), title=title, posts=[post], following_post=following_post)
        return render_template('random_post.html.j2', category=_('Article'), title=title, posts=[post], following_post=False)
    return render_template('random_post.html.j2', category=_('Article'), title=title, posts=[], following_post=False)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.keyword.data
        page_num = request.args.get('page', 1, type=int)
        posts = Post.query.filter(Post.title.like(f'%{keyword}%')).paginate(
            page=page_num, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
        next_url = url_for('search', keyword=keyword,
                           page=page_num + 1) if posts.has_next else None
        prev_url = url_for('search', keyword=keyword,
                           page=page_num - 1) if posts.has_prev else None
        return render_template('search.html.j2', title=_('Search results'), posts=posts.items, keyword=keyword, next_url=next_url, prev_url=prev_url)
    return render_template('search.html.j2', title=_('Search'), form=form)


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    form = DonationForm()
    count_total = None
    if form.validate_on_submit():
        option = form.once_or_monthly.data
        amount = form.amount.data
        fee = form.transaction_fee.data
        count_total = int(amount)
        if fee:
            count_total *= 1.04  # Amount+交易手續費
        if form.card.data:
            pay_method = 'card'
        elif form.paypal.data:
            pay_method = 'paypal'
        else:
            pay_method = 'Payme'
        return redirect(url_for('payment', pay_method=pay_method, amount=count_total,option=str(option), donate_form=form))
    return render_template('donate.html.j2', form=form)


@app.route('/payment/<pay_method>/<amount>/<option>', methods=['GET', 'POST'])
def payment(pay_method, amount, option):
    payment_form = PaymentForm(submit=pay_method)
    if payment_form.validate_on_submit():
        firstname=payment_form.firstname.data
        lastname=payment_form.lastname.data
        email=payment_form.email.data
        donate_on=datetime.utcnow()
        pay_acc=payment_form.pay_acc.data
        if option == "monthly":
            monthly = True
        else:
            monthly = False
        donor = Donor(firstname=firstname, lastname=lastname, email=email, monthly=monthly)
        db.session.add(donor)
        db.session.commit()
        return redirect(url_for('payment_loading', firstname=firstname,lastname=lastname,donate_on=donate_on,pay_acc=pay_acc,pay_method=pay_method,amount=amount))
    elif request.method == 'GET':
        payment_form.submit.label.text = f'Donate with {pay_method}'
    return render_template('donate_payment.html.j2', form=payment_form, amount=amount)

@app.route('/payment_loading/<firstname>/<lastname>/<donate_on>/<pay_acc>/<pay_method>/<amount>', methods=['GET','POST'])
def payment_loading(firstname,lastname,donate_on,pay_acc,pay_method,amount):
    donor = Donor.query.filter_by(firstname=firstname,lastname=lastname).first() or None
    if donor:
        payment=Payment(donor_id=donor.id,donate_on=donate_on, \
                        pay_method=pay_method, pay_acc=pay_acc, amount=amount)
        flash('Thank you for your donation!')
        db.session.add(payment)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/leave_message', methods=['GET', 'POST'])
def leave_message():
    LMform=LeaveMessageForm()
    if LMform.validate_on_submit():
        name =LMform.name.data
        message =LMform.message.data
        leave_msg = Leave_message(name=name, message=message)
        db.session.add(leave_msg)
        db.session.commit()
        flash('Message Sent Successfully!')
        return redirect(url_for('leave_message'))
    page_num = request.args.get('page', 1, type=int)
    events = Leave_message.query.paginate(
        page=page_num, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for('leave_message', page=page_num + 1) if events.has_next else None
    prev_url = url_for('leave_message', page=page_num - 1) if events.has_prev else None
    return render_template('leave_message.html.j2',title=_('Leave a Message...'), form=LMform, events=events.items, next_url=next_url, prev_url=prev_url)


@app.route('/lessons')
def lessons():
    # lessons = Lesson.query.all()
    return render_template('lessons.html.j2', lessons=lessons)

@app.route('/lessons_list')
def lessons_list():
    lessons = Lesson.query.all()
    return render_template('lessons_list.html.j2', lessons=lessons)

@app.route('/practice')
def practice():
    return render_template('practice.html.j2')

@app.route('/dictionary')
def dictionary():
    return render_template('dictionary.html.j2')

@app.route('/community')
def community():
    return render_template('community.html.j2')

@app.route('/chat_with_copilot', methods=['GET', 'POST'])
def chat_with_copilot():
    if request.method == 'POST':
        word_limit = request.form.get('word-limit')
        if word_limit:
            try:
                word_limit = int(word_limit)
            except ValueError:
                word_limit = 50  # 預設值
        else:
            word_limit = 50  # 預設值
        
        condition = request.form.get('condition')
        debug = request.form.get('debug', 'false').lower() == 'true'
        
        # Log values to console for debugging
        # print('Debug:', debug)
        # print('Word Limit:', word_limit)
        # print('Condition:', condition)
        
        # Update the single ChatSettings record
        chat_settings = ChatSettings.query.first()
        if chat_settings is None:
            chat_settings = ChatSettings(debug=debug, word_limit=word_limit, condition=condition)
            db.session.add(chat_settings)
        else:
            chat_settings.debug = debug
            chat_settings.word_limit = word_limit
            chat_settings.condition = condition
            chat_settings.timestamp = datetime.utcnow()
        db.session.commit()
        
        if 'message' in request.form:
            input_text = request.form.get('message')
            chrome_driver_path = "./chromedriver-linux64/chromedriver"
            copilot = CopilotChat(chrome_driver_path, debug=debug)
            response_text = copilot.chat(input_text, word_limit, condition)
            if response_text is None:
                response_text = _('An error occurred while processing your request. Please try again later.')
            return jsonify({'response': response_text})
        else:
            flash(_('Settings updated successfully.'))
            return redirect(url_for('chat_with_copilot'))
    
    # Get the latest settings
    chat_settings = ChatSettings.query.first()
    return render_template('chat_with_copilot.html.j2', chat_settings=chat_settings)

@app.route('/set_language', methods=['POST'])
def set_language():
    lang = request.form.get('language')
    if lang:
        session['lang'] = lang
        refresh()
    return redirect(request.referrer)

@app.route('/record')
@login_required
def record():
    evaluation = session.pop('evaluation', None)  # Retrieve and remove evaluation from session
    return render_template('record.html.j2', evaluation=evaluation)

@app.route('/video_evaluation', methods=['POST'])
def video_evaluation():
    if 'video' not in request.files:
        flash('No video file provided')
        return jsonify({'success': False, 'message': 'No video file provided'})

    video = request.files['video']
    mime_type, _ = guess_type(video.filename)
    allowed_mime_types = [
        'video/mp4', 'video/mpeg', 'video/mov', 'video/avi', 'video/x-flv',
        'video/mpg', 'video/webm', 'video/wmv', 'video/3gpp'
    ]
    if not mime_type or mime_type not in allowed_mime_types:
        flash('Unsupported file format, please upload again!')
        return jsonify({'success': False, 'message': 'Unsupported file format'})

    video_path = os.path.join(current_app.root_path, 'static/video', secure_filename(video.filename))
    try:
        video.save(video_path)
    except Exception as e:
        current_app.logger.error(f'Error saving video: {e}')
        flash('Error saving video')
        return jsonify({'success': False, 'message': 'Error saving video'})

    gemini_client = GeminiClient()
    try:
        evaluation_response = gemini_client.evaluate_video(video.filename)
        current_app.logger.info(f'Evaluation response: {evaluation_response}')
        if evaluation_response:
            evaluation_data = evaluation_response  # 已由 GeminiClient 處理格式
            current_app.logger.info(f'Evaluation data: {evaluation_data}')

            # Save evaluation data to the database
            evaluation = Evaluation(
                user_id=current_user.id,
                pronunciation_accuracy=evaluation_data['evaluation_criteria']['pronunciation_accuracy']['score'],
                grammar_usage=evaluation_data['evaluation_criteria']['grammar_usage']['score'],
                vocabulary_usage=evaluation_data['evaluation_criteria']['vocabulary_usage']['score'],
                fluency=evaluation_data['evaluation_criteria']['fluency']['score'],
                comprehension=evaluation_data['evaluation_criteria']['comprehension']['score'],
                jlpt_level=evaluation_data['evaluation_criteria']['jlpt_level']['score'],
                passing_probability_n1=evaluation_data['summary']['passing_probability']['N1'],
                passing_probability_n2=evaluation_data['summary']['passing_probability']['N2'],
                passing_probability_n3=evaluation_data['summary']['passing_probability']['N3'],
                passing_probability_n4=evaluation_data['summary']['passing_probability']['N4'],
                passing_probability_n5=evaluation_data['summary']['passing_probability']['N5'],
                feedback_and_recommendations=evaluation_data['summary']['feedback_and_recommendations']
            )
            db.session.add(evaluation)
            db.session.commit()
            user_id = current_user.id
            return jsonify({'success': True, 'user_id': user_id})
        else:
            current_app.logger.error('No valid JSON found in the response')
            return jsonify({'success': False, 'message': 'No valid JSON found in the response'})
    except Exception as e:
        current_app.logger.error(f'Error evaluating video: {e}')
        return jsonify({'success': False, 'message': 'Error evaluating video'})

    current_app.logger.info('Redirecting to record page')
    return jsonify({'success': False, 'message': 'Unknown error'})

@app.route('/score/<int:user_id>', methods=['GET'])
@login_required
def score(user_id):
    evaluations = Evaluation.query.filter_by(user_id=user_id).order_by(Evaluation.id.desc()).all()
    current_app.logger.info(f'Evaluations retrieved from database: {evaluations}')
    return render_template('score.html.j2', evaluations=evaluations)

@app.route('/charts')
def charts():
    # 定義數據
    labels = ['A', 'B', 'C', 'D', 'E']
    values1 = [4, 3, 5, 2, 4]  # 第一組數據
    values2 = [3, 4, 2, 5, 3]  # 第二組數據
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values1 += values1[:1]
    angles += angles[:1]

    # 繪製雷達圖和長條圖
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), subplot_kw={'polar': True})  # 第一子圖為極坐標

    # 第一個子圖：雷達圖
    ax_radar = axes[0]
    ax_radar.plot(angles, values1, linewidth=2, linestyle='solid', color='blue', label='Group 1')
    ax_radar.fill(angles, values1, color='blue', alpha=0.25)
    ax_radar.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax_radar.set_facecolor('black')  # 背景顏色
    ax_radar.tick_params(colors='white')  # 字體顏色
    ax_radar.legend(labelcolor='white')

    # 第二個子圖：長條圖 (非極坐標，所以不使用 'polar')
    fig.delaxes(axes[1])  # 刪除默認的第二極坐標子圖
    ax_bar = fig.add_subplot(1, 2, 2)  # 添加普通的笛卡爾坐標系
    ax_bar.bar(labels, values2, color='palegreen')  # 繪製長條圖
    ax_bar.set_facecolor('black')  # 背景顏色
    ax_bar.tick_params(colors='white')  # 字體顏色
    ax_bar.set_title('Bar Chart', color='white')  # 設置標題

    # 設置圖紙背景顏色
    fig.patch.set_facecolor('black')

    # 保存圖表為圖片
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_data = buf.getvalue()
    buf.close()

    # 將圖表數據傳遞給模板
    chart_data_base64 = f"data:image/png;base64,{base64.b64encode(chart_data).decode('utf-8')}"
    return render_template('charts.html.j2', chart_data=chart_data_base64)

@app.route('/check_character', methods=['POST'])
def check_character():
    data = request.get_json()
    if not data or 'targetCharacter' not in data or 'handwritingImage' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    target_character = data['targetCharacter']
    handwriting_image = data['handwritingImage']
    
    print(f"target_character: {target_character}")

    try:
        # Save the handwriting image temporarily
        image_path = os.path.join(current_app.root_path, 'static', 'image', 'handwriting.png')
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(handwriting_image.split(",")[1]))

        # Use GeminiClient to compare handwriting with the target character
        gemini_client = GeminiClient()
        response_data = gemini_client.compare_handwriting('handwriting.png', target_character)
        
        if response_data:
            # Extract score and feedback
            similarity_score = response_data.get("similarity_score", {}).get("score", "N/A")
            feedback = response_data.get("feedback", "No feedback provided.")
        else:
            current_app.logger.error('No valid JSON found in the response')
            return jsonify({'error': 'No valid JSON found in the response'}), 500

        # Clean up the temporary file
        os.remove(image_path)

        return jsonify({
            'similarity_score': similarity_score,
            'feedback': feedback
        })

    except Exception as e:
        current_app.logger.error(f'Error during character comparison: {e}')
        return jsonify({'error': 'An error occurred while processing your handwriting.'}), 500

@app.route('/save_handwriting', methods=['POST'])
def save_handwriting():
    data = request.get_json()
    handwriting_image = data.get('handwritingImage')
    target_character = data.get('targetCharacter')

    if not handwriting_image or not target_character:
        return jsonify({'error': 'Invalid data'}), 400

    # Decode the Base64 image
    try:
        image_data = base64.b64decode(handwriting_image.split(',')[1])
        image_path = os.path.join('app', 'static', 'image', 'handwriting.png')

        # Save the image to the specified path
        with open(image_path, 'wb') as f:
            f.write(image_data)

        # Mock similarity score and feedback for demonstration
        similarity_score = 85  # Example score
        feedback = f"The character '{target_character}' is well-written!"

        return jsonify({'similarity_score': similarity_score, 'feedback': feedback}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
