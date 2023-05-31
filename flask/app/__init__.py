from flask import Flask

app = Flask(__name__)

from config import config
app.config.from_object(config.Config)

app.jinja_env.globals.update(round=round, enumerate=enumerate, range=range)

from app import routes