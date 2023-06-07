# run.py

from app import app
from config.config import Config

app.config.from_object(Config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
