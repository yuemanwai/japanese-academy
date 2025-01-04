from datetime import datetime, timedelta, timezone
from hashlib import md5
from app import app, db, login
import jwt
from flask import make_response
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash


watchlist = db.Table(
    'watchlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'),nullable=False)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    login_count = db.Column(db.Integer, default=0)
    fail_login_count = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
        

    def __repr__(self) -> str:
        return f'<Username : {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, post):
        if not self.is_following(post):
            self.posts.append(post)

    def unfollow(self, post):
        if self.is_following(post):
            self.posts.remove(post)

    def is_following(self, post):
        return self.posts.filter(watchlist.c.post_id == post.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            watchlist, watchlist.c.post_id == Post.id
        ).filter(watchlist.c.user_id == self.id)
        return followed.order_by(Post.create_time.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id,
                           "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)},
                          app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")[
                "reset_password"]
        except:           
            return None
        return User.query.get(id)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True, unique=True)
    body = db.Column(db.String(2000))
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    edit_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    edit_count = db.Column(db.Integer, default=0)
    protected = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    users = db.relationship('User', secondary=watchlist,
                        backref=db.backref('posts', lazy='dynamic'),
                        primaryjoin=(watchlist.c.post_id == id),
                        secondaryjoin=(watchlist.c.user_id == User.id),
                        lazy='dynamic')

    user = db.relationship('User', backref='user_posts', lazy=True)

    def __repr__(self) -> str:
        return f'<Post title : {self.title}>'
    

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    donate_on = db.Column(db.DateTime, nullable=False)
    pay_method = db.Column(db.String(50), nullable=False)
    pay_acc = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Payment(id={self.id}, donor_id='{self.donor_id}, pay_method='{self.pay_method}, amount_hkd='{self.amount_hkd}')>"

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    monthly = db.Column(db.Boolean, nullable=False)

    payments = db.relationship('Payment', backref='donor', lazy=True)

    def __repr__(self):
        return f"<Donor(id={self.id}, firstname='{self.firstname}, lastname='{self.lastname}, monthly='{self.monthly}')>"

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    nationality = db.Column(db.String(50))
    books = db.relationship('Editor', backref='author', lazy=True)
 
    def _repr_(self):
        return f"Author(id={self.id}, name='{self.name}')"
    
class Editor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    publication_date = db.Column(db.Date)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def _repr_(self):
        return f"Category(id={self.id}, name='{self.name}')"
    

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def _repr_(self):
        return f"Vote(id={self.id}, value={self.value})"

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(20), nullable=False)

    def _repr_(self):
        return f"History(id={self.id}, action='{self.action}')"

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"Tag(id={self.id}, name='{self.name}')"

class Revision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer,  nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Revision(id={self.id})"


# class UserSession(db.Model): # 如果要係db放session_id...
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     session_id = db.Column(db.PickleType)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True, unique=True, nullable=False)
    filename = db.Column(db.String(100), index=True, unique=True, nullable=False)

    def __repr__(self):
        return f"<Image(id={self.id}, post_id={self.post_id}, filename='{self.filename}')>"
    

class IP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True, unique=True, nullable=False)
    ip_addr = db.Column(db.String(50), index=True, unique=True, nullable=False)

    def __repr__(self):
        return f"<IP(id={self.id}, post_id={self.post_id}, ip='{self.ip}')>"
    

    
class Leave_message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    message = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Leave_message(id={self.id}, name='{self.name}, message='{self.message}')>"




# 呢度新係加

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Instructor(id={self.id}, name='{self.name}')>"

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Level(id={self.id}, name='{self.name}')>"

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=True)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)

    instructor = db.relationship('Instructor', backref='lessons')
    level = db.relationship('Level', backref='lessons')

    def __repr__(self):
        return f"<Lesson(id={self.id}, name='{self.name}')>"

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), index=True, unique=True, nullable=False)

    def __repr__(self):
        return f"<Link(id={self.id}, name='{self.name}'), link='{self.link}'>"

class ChatSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debug = db.Column(db.Boolean, default=False)
    headless = db.Column(db.Boolean, default=True)
    word_limit = db.Column(db.Integer, default=50)
    condition = db.Column(db.String(255), default="answer using only text and in simple japanese(and explain what you mean in short eng)")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)