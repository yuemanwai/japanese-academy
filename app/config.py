import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    
    # PostgreSQL 連接參數
    DB_HOST = os.environ.get("DB_HOST") or "postgresdb"
    DB_PORT = os.environ.get("DB_PORT") or "5432"
    DB_NAME = os.environ.get("DB_NAME") or "postgres"
    DB_USER = os.environ.get("DB_USER") or "postgres"
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or "postgres"
    
    # 如果有完整的 DATABASE_URI，使用它；否則從分別的參數構建
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or \
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # === 新增：解決 flask-session 與 PostgreSQL 系統命名衝突 ===
    # 將 Session Table 名稱從默認的 'sessions' 改為一個獨特且安全的名稱。
    SESSION_SQLALCHEMY_TABLE = 'flask_sessions_data' 


    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "mailhog"
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 1025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@example.com']
    POSTS_PER_PAGE = 10
    LANGUAGES = ['en', 'es', 'zh']
    RECAPTCHA_PUBLIC_KEY='no-key'
    RECAPTCHA_PRIVATE_KEY='no-key'
    
    # API Keys
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
