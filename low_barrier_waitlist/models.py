# -*- coding: utf-8 -*-
import datetime

import pytz
from flask_security import RoleMixin, UserMixin

from . import db
from .utils import one_week_ago


class Participant(db.Document):
    hmis = db.StringField(unique=True)
    age = db.IntField(required=True)
    disability_status = db.BooleanField(required=True)
    veteran = db.BooleanField(required=True)
    gender = db.StringField(required=True)
    checkin_datetime = db.DateTimeField(null=True)
    assigned_bed = db.BooleanField(required=True, default=False)

    meta = {"indexes": ["hmis", "-checkin_datetime"]}

    def check_in(self):
        self.checkin_datetime = datetime.datetime.now(tz=pytz.utc)

    @db.queryset_manager
    def bed_eligable(doc_cls, queryset):
        return queryset.filter(
            checkin_datetime__gte=one_week_ago(), assigned_bed=False
        )


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
