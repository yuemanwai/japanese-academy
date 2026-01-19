import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
import sys
from flask import Flask, request, session
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_session import Session
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app, 
    group_by='endpoint',
    excluded_paths=['/healthz', '/health', '/readyz', '/ready', '/metrics', '/startup']
)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
Session(app)
migrate = Migrate(app, db)
login = LoginManager()
login.login_view = "login"
login.init_app(app)
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel()
babel.init_app(app, locale_selector=lambda: session.get('lang', 'en'))

if not app.debug:
    root = logging.getLogger()
    
    # 獲取 log level，優先使用環境變數，否則使用 config，默認為 INFO
    log_level_name = os.environ.get('LOG_LEVEL') or app.config.get('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level_name.upper(), logging.INFO)
    
    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='App Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        root.addHandler(mail_handler)

    # 修改部分開始: 將 Log 輸出到 stdout
    # 判斷是否開啟 STDOUT (避免環境變數字串 "false" 被誤判為 True)
    to_stdout = os.environ.get('LOG_TO_STDOUT', '').lower() in ['true', '1', 'on'] \
                or app.config.get('LOG_TO_STDOUT') is True
    
    if to_stdout:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        stream_handler.setLevel(log_level)
        root.addHandler(stream_handler)
    else:
        # 這裡保留舊邏輯作為 fallback，或者你可以直接刪除 RotatingFileHandler
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/App.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(log_level)
        root.addHandler(file_handler)

    root.setLevel(log_level)
    root.info('App startup')

# You must keep the routes at the end.
from app import routes, errors
