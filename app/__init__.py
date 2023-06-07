from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Access the SECRET_KEY value
SECRET_KEY = os.getenv("SECRET_KEY")

app.config['SECRET_KEY'] = SECRET_KEY

app.jinja_env.globals.update(round=round, enumerate=enumerate, range=range)

from app import routes