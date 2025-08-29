from app import app
import os

if __name__ == '__main__':
    # Use 127.0.0.1 for production safety, 0.0.0.0 only in dev containers
    host = '0.0.0.0' if os.environ.get('FLASK_ENV') == 'development' or os.environ.get('CODESPACES') else '127.0.0.1'
    app.run(host=host, port=5000, debug=False)

    
