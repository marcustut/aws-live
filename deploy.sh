#!/bin/bash

pip install pipenv 

pipenv install python-dotenv --dev
pipenv install flask flask_expects_json pymysql boto3 argon2-cffi faker
pipenv shell

python app.py
