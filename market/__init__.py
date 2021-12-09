from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session
import redis
import hvac

from os import environ

vault_client = hvac.Client(url='https://vault.westconcloud-id.net:8200', token=environ.get['VAULT_TOKEN'])
vault_data = vault_client.read(path='kv/data/flask-market/app')

db_user = vault_data['data']['data']['app_db_user']
db_pass = vault_data['data']['data']['app_db_pwd']
db_host = vault_data['data']['data']['app_db_host']
redis_host = vault_data['data']['data']['app_redis_host']


db_uri = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/flaskmarket"
redis_url = f"redis://{redis_host}:6379"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5e28012199438177276dc0fa'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_REDIS'] = redis.from_url(redis_url)

server_session = Session(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes
