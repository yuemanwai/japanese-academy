import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

basedir = os.path.abspath(os.path.dirname(__file__))


def get_database_uri():
    """
    獲取數據庫連接字串。
    優先級 1: 環境變數 SQLALCHEMY_DATABASE_URI (Local/Test)
    優先級 2: AWS Secrets Manager (Production)
    """

    # === 1. Local Mode ===
    # 如果直接提供了完整的 URI，直接使用並返回
    local_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")
    if local_uri:
        print(f"[INFO] Using SQLALCHEMY_DATABASE_URI from environment variables.")
        return local_uri

    # === 2. AWS Mode Preparation ===
    print("[INFO] No local URI found. Preparing to fetch from AWS Secrets Manager...")

    # 獲取必要的 AWS 配置
    secret_name = os.environ.get("AWS_SECRET_NAME")
    region_name = os.environ.get("AWS_REGION")

    # === 3. Validation (防呆檢查) ===
    # 檢查是否缺少必要的環境變數，如果有缺，立即報錯
    missing_vars = []
    if not secret_name:
        missing_vars.append("AWS_SECRET_NAME")
    if not region_name:
        missing_vars.append("AWS_REGION")

    if missing_vars:
        # 這裡會直接拋出錯誤，阻止 App 啟動
        error_msg = f"[CRITICAL] Missing required environment variables for AWS Mode: {', '.join(missing_vars)}"
        print(error_msg)
        raise ValueError(error_msg)

    # === 4. Boto3 Execution ===
    try:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)

        print(f"[INFO] Fetching secret '{secret_name}' from region '{region_name}'...")
        response = client.get_secret_value(SecretId=secret_name)

        if 'SecretString' in response:
            secret = json.loads(response['SecretString'])

            # 必需鍵檢查
            required_keys = ['username', 'password', 'host', 'dbname']
            if not all(k in secret for k in required_keys):
                raise KeyError(f"Secret JSON is missing one of the required keys: {required_keys}")

            # 使用 secret 中的端口，如果沒有指定則預設為 5432
            port = secret.get('port', 5432)
            return f"postgresql://{secret['username']}:{secret['password']}@{secret['host']}:{port}/{secret['dbname']}"
        else:
            # 處理 SecretBinary 情況（雖然不太可能）
            raise ValueError("Secret must be in SecretString format, not SecretBinary")

    except (NoCredentialsError, ClientError) as e:
        # 捕捉 AWS 相關的錯誤 (例如 IRSA 失敗，或者 Secret Name 錯誤)
        print(f"[CRITICAL] Failed to retrieve secret from AWS: {e}")
        raise e
    except Exception as e:
        # 捕捉 JSON 解析或其他未知錯誤
        print(f"[CRITICAL] Unexpected error during database configuration: {e}")
        raise e


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        import sys
        print("[CRITICAL] SECRET_KEY environment variable is not set. This is required for production security.")
        print("[INFO] For development, set a random SECRET_KEY. Example: export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')")
        if os.environ.get("FLASK_ENV") == "production":
            raise ValueError("[CRITICAL] SECRET_KEY must be set in production environment")
        # For development, we can proceed with a warning, but never use hardcoded default
    
    # 優先從環境變數或 AWS Secrets Manager 取得資料庫連線字串
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    
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
    # RECAPTCHA_PUBLIC_KEY='no-key'
    # RECAPTCHA_PRIVATE_KEY='no-key'
    
    # API Keys
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
