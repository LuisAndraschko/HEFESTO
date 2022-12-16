from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '47665f0caf395f8b7cfb54faac032245'

app.jinja_env.globals.update(round=round)

from app import routes