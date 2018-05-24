from datetime import datetime

import pytz

from . import db


class Participant(db.Document):
    hmis = db.StringField(
        min_length=4, max_length=12, unique=True, primary_key=True
    )
    age = db.IntField(required=True)
    disability_status = db.BooleanField(required=True)
    veteran = db.BooleanField(required=True)
    gender = db.StringField(required=True, choices={"Male", "Female"})
    checkin_datetime = db.DateTimeField(null=True)
    assigned_bed = db.BooleanField(required=True, default=False)

    def check_in(self):
        self.checkin_datetime = datetime.now(tz=pytz.utc)
