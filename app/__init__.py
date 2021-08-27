import json

with open('app/config/app-config.json', 'r') as f:
    app_config = json.load(f)
with open('app/config/email-config.json', 'r') as f:
    email_config = json.load(f)
with open('app/config/database-config.json', 'r') as f:
    database_config = json.load(f)

from flask import Flask, session
main = Flask(__name__)
main.secret_key = app_config['app-secret-key']
main.config.update(
    MAIL_SERVER=email_config['server'],
    MAIL_PORT=email_config['port'],
    MAIL_USE_SSL=email_config['use-ssl'],
    MAIL_USERNAME=email_config['username'],
    MAIL_PASSWORD=email_config['password']
)

from .login import login
main.register_blueprint(login)
from .bitly import bitly
main.register_blueprint(bitly)