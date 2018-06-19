# -*- coding: utf-8 -*-
import os

UPLOAD_FOLDER = "/tmp"
ALLOWED_EXTENSIONS = {"csv"}

SECURITY_LOGIN_URL = "/admin/login"
SECURITY_LOGIN_USER_TEMPLATE = "login_user.html"
SECURITY_LOGOUT_URL = "/admin/logout"
SECURITY_REGISTER_URL = "/admin/register"
SECURITY_RESET_URL = "/admin/password_reset"
SECURITY_CHANGE_URL = "/admin/change_password"
SECURITY_CONFIRM_URL = "/admin/confirm"
SECURITY_POST_LOGIN_VIEW = "/admin"
SECURITY_POST_LOGOUT_VIEW = "/"


if os.environ.get("TESTING", False):
    DEBUG = True
    MONGODB_DB = "test"
    SECRET_KEY = "FOOOOOOOO"
    SECURITY_PASSWORD_SALT = "salty"
else:
    MONGODB_DB = "low_barrier_waitlist"
    SECRET_KEY = "<REPLACE_ME_SECRET_KEY>"
    SECURITY_PASSWORD_SALT = "<REPLACE_ME_PASSWORD_SALT>"
