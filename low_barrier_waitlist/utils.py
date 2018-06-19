# -*- coding: utf-8 -*-
import os
import sys
import logging
import datetime


def configure_logging():
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


def one_week_ago():
    td = datetime.timedelta(weeks=1)
    return datetime.datetime.combine(
        datetime.date.today() - td, datetime.datetime.min.time()
    )
