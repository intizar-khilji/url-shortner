from flask import Blueprint
bitly = Blueprint('bitly', __name__, template_folder='./templates', static_folder='static', static_url_path='/static/bitly')
home_url = 'bitly.home'
from . import routes, function, database