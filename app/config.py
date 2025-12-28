import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from urllib.parse import quote_plus

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
    
    # 從環境變數取得資料庫 Host / DB 名稱與 Port（Port 預設 5432）
    def _get_env(names, default=None):
        for n in names:
            v = os.environ.get(n)
            if v:
                return v
        return default

    env_host = _get_env(["DB_HOST", "POSTGRES_HOST", "PGHOST"])  # Host 由環境取得
    env_dbname = _get_env(["DB_NAME", "POSTGRES_DB"])             # DB 名稱由環境取得
    env_port = _get_env(["DB_PORT", "POSTGRES_PORT", "PGPORT"], 5432)  # Port 先由 env 取得，沒有就預設 5432
    try:
        env_port = int(env_port) if env_port is not None else 5432
    except ValueError:
        print(f"[WARN] Invalid DB port value '{env_port}' in env. Falling back to 5432.")
        env_port = 5432

    # === 3. Validation (防呆檢查) ===
    # 檢查是否缺少必要的環境變數，如果有缺，立即報錯
    missing_vars = []
    if not secret_name:
        missing_vars.append("AWS_SECRET_NAME")
    if not region_name:
        missing_vars.append("AWS_REGION")
    if not env_host:
        missing_vars.append("DB_HOST/POSTGRES_HOST/PGHOST")
    if not env_dbname:
        missing_vars.append("DB_NAME/POSTGRES_DB")

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

            # 必需鍵檢查（使用者名稱與密碼由 Secret 取得；host/dbname 由環境取得）
            required_keys = ['username', 'password']
            if not all(k in secret for k in required_keys):
                raise KeyError(f"Secret JSON is missing one of the required keys: {required_keys}")

            # Port 優先由環境變數取得，若無則預設 5432
            port = env_port
            # 將憑證與 dbname 使用 URL 安全編碼，避免特殊字元造成解析問題
            quoted_username = quote_plus(str(secret['username']))
            quoted_password = quote_plus(str(secret['password']))
            quoted_dbname = quote_plus(str(env_dbname))
            # 組合最終連線字串：username/password 來自 Secret；host/dbname 來自環境；port 來自環境或 5432
            return f"postgresql://{quoted_username}:{quoted_password}@{env_host}:{port}/{quoted_dbname}"
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
        # 在開發環境中允許沒有 SECRET_KEY（會產生警告），但在生產環境中強制要求
        if os.environ.get("FLASK_ENV") == "production":
            raise ValueError("[CRITICAL] SECRET_KEY must be set in production environment")
        else:
            # 開發環境：使用臨時的 secret key，並發出警告
            import secrets
            SECRET_KEY = secrets.token_hex(32)
            print("[WARN] SECRET_KEY not set in development. Using temporary key. Set SECRET_KEY env var for persistence.")
    
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
