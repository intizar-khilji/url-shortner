import json
with open('app/config/database-config.json', 'r') as f:
    database_config = json.load(f)

from flask import Blueprint
login = Blueprint('login', __name__, template_folder='./templates', static_folder='static', static_url_path='/static/login')
home_url = 'bitly.home'
from . import routes, database, functions