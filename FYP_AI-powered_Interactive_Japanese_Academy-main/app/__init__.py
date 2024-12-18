from flask import Flask
from flask_bootstrap import Bootstrap
from flask_babel import Babel

app = Flask(__name__)
boostrap = Bootstrap(app=app)
babel = Babel(app)


from app import routes, errors
