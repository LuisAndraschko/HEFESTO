# run.py

from app import app
from config.config import Config

app.config.from_object(Config)

if __name__ == '__main__':
    app.run()