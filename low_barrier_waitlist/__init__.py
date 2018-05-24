from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object("config")
csrf = CSRFProtect(app)
mongo = PyMongo(app)

from . import views
