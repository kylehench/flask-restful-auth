from flask import Flask
import os
app = Flask(__name__)
app.SECRET_KEY = os.environ.get('SECRET_KEY')
app.BASE_DIRECTORY = os.environ.get('BASE_DIRECTORY')
print(app.BASE_DIRECTORY)