import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from urllib.parse import quote_plus

basedir = os.path.abspath(os.path.dirname(__file__))

# boto3 AWS Secrets Manager 參考文件
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_secret_value.html

def get_database_uri():
    """
    獲取數據庫連接字串。
    自動檢測運行模式：
        - 若存在 AWS_SECRET_NAME 和 AWS_REGION，使用 AWS Secrets Manager (Production)
        - 若不存在，使用本地環境變數 (Local/Test)
    兩種模式都只接受拼接的 URI，從環境變數組合而成。
    """
    
    # Helper function: 從多個可能的環境變數名稱中取值
    def _get_env(names, default=None):
        for n in names:
            v = os.environ.get(n)
            if v:
                return v
        return default

    # 從環境變數取得資料庫 Host / DB 名稱與 Port（Port 預設 5432）
    env_host = _get_env(["DB_HOST", "POSTGRES_HOST", "PGHOST"])
    env_dbname = _get_env(["DB_NAME", "POSTGRES_DB"])
    env_port = _get_env(["DB_PORT", "POSTGRES_PORT", "PGPORT"], 5432)
    try:
        env_port = int(env_port) if env_port is not None else 5432
    except ValueError:
        print(f"[WARN] Invalid DB port value '{env_port}' in env. Falling back to 5432.")
        env_port = 5432

    # 檢查是否存在 AWS 配置
    secret_name = os.environ.get("AWS_SECRET_NAME")
    region_name = os.environ.get("AWS_REGION")

    # === 1. AWS Secrets Manager Mode (若存在 AWS_SECRET_NAME 和 AWS_REGION) ===
    if secret_name and region_name:
        print("[INFO] AWS credentials detected. Running in AWS Secrets Manager mode...")

        # 檢查是否缺少必要的環境變數
        missing_vars = []
        if not env_host:
            missing_vars.append("DB_HOST/POSTGRES_HOST/PGHOST")
        if not env_dbname:
            missing_vars.append("DB_NAME/POSTGRES_DB")

        if missing_vars:
            error_msg = f"[CRITICAL] Missing required environment variables for AWS Mode: {', '.join(missing_vars)}"
            print(error_msg)
            raise ValueError(error_msg)

        # Boto3 Execution
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

                # 將憑證與 dbname 使用 URL 安全編碼，避免特殊字元造成解析問題
                quoted_username = quote_plus(str(secret['username']))
                quoted_password = quote_plus(str(secret['password']))
                quoted_dbname = quote_plus(str(env_dbname))
                # 組合最終連線字串：username/password 來自 Secret；host/dbname 來自環境；port 來自環境或 5432
                return f"postgresql://{quoted_username}:{quoted_password}@{env_host}:{env_port}/{quoted_dbname}"
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

    # === 2. Local/Test Mode (若不存在 AWS_SECRET_NAME 或 AWS_REGION) ===
    else:
        print("[INFO] No AWS credentials found. Running in Local/Test mode...")
        print("[INFO] Composing database URI from environment variables...")
        
        local_username = _get_env(["DB_USERNAME", "POSTGRES_USER"])
        local_password = _get_env(["DB_PASSWORD", "POSTGRES_PASSWORD"])
        
        # 檢查必要的環境變數
        missing_vars = []
        if not local_username:
            missing_vars.append("DB_USERNAME/POSTGRES_USER")
        if not local_password:
            missing_vars.append("DB_PASSWORD/POSTGRES_PASSWORD")
        if not env_host:
            missing_vars.append("DB_HOST/POSTGRES_HOST/PGHOST")
        if not env_dbname:
            missing_vars.append("DB_NAME/POSTGRES_DB")
        
        if missing_vars:
            error_msg = f"[CRITICAL] Missing required environment variables for Local/Test Mode: {', '.join(missing_vars)}"
            print(error_msg)
            raise ValueError(error_msg)
        
        # 組合 URI
        quoted_username = quote_plus(str(local_username))
        quoted_password = quote_plus(str(local_password))
        quoted_dbname = quote_plus(str(env_dbname))
        return f"postgresql://{quoted_username}:{quoted_password}@{env_host}:{env_port}/{quoted_dbname}"


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        print("[WARN] SECRET_KEY not set. Generated temporary key. Set SECRET_KEY env var for persistence.")
    
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
