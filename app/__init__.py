# __init__.py
from flask import Flask

app = Flask(__name__, static_url_path='/static')

from config import config
app.config.from_object(config.Config)

app.jinja_env.globals.update(round=round, enumerate=enumerate, range=range)

from app import routes