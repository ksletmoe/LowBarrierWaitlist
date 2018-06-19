# -*- coding: utf-8 -*-
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security

from .utils import configure_logging

configure_logging()

app = Flask(__name__)
app.config.from_object("config")
csrf = CSRFProtect(app)
db = MongoEngine(app)

from .models import User, Role

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from . import views
