import datetime

import pytz

from . import db


class Participant(db.Document):
    hmis = db.StringField(min_length=4, max_length=12, unique=True)
    age = db.IntField(required=True)
    disability_status = db.BooleanField(required=True)
    veteran = db.BooleanField(required=True)
    gender = db.StringField(required=True, choices={"Male", "Female"})
    checkin_datetime = db.DateTimeField(null=True)
    assigned_bed = db.BooleanField(required=True, default=False)

    meta = {"indexes": ["hmis"]}

    def check_in(self):
        self.checkin_datetime = datetime.datetime.now(tz=pytz.utc)

    @db.queryset_manager
    def bed_eligable(doc_cls, queryset):
        return queryset.filter(
            checkin_datetime__gte=one_week_ago(), assigned_bed=False
        )


def one_week_ago():
    td = datetime.timedelta(weeks=1)
    return datetime.datetime.combine(
        datetime.date.today() - td, datetime.datetime.min.time()
    )
