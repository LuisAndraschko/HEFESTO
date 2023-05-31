# config/config.py
import os

class Config:
    SECRET_KEY = '47665f0caf395f8b7cfb54faac032245'
    # SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    # Add other configuration settings specific to your deployment environment

