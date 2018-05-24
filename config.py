import os

SECRET_KEY = "FOOOOOOOO"
UPLOAD_FOLDER = "/tmp"
ALLOWED_EXTENSIONS = set(["csv"])

if os.environ.get("TESTING", False):
    DEBUG = True
    MONGODB_DB = "test"
else:
    MONGODB_DB = "low_barrier_waitlist"
