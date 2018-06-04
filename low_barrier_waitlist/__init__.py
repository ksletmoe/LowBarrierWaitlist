import os
import sys
import logging

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config.from_object("config")
csrf = CSRFProtect(app)
db = MongoEngine(app)

flask_env = os.environ.get("FLASK_ENV", None)
if flask_env and flask_env == "development":
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

logging.basicConfig(
    stream=sys.stderr,
    format="%(asctime)s - %(levelname)s: %(message)s",
    level=log_level,
)

from . import views
