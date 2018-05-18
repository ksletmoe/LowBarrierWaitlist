import json
from datetime import datetime

import pytz


class Model:
    def __init__(self, attributes):
        self.attributes = attributes

    def dump(self):
        return json.dumps(self.attributes)

    def __getattr__(self, name):
        return self.attributes.get(name)

    def load(self, object):
        raise NotImplementedError('Implement in child model')


class Participant(Model):
    def __init__(self,
                 hmis,
                 age,
                 disability_status,
                 veteran,
                 gender,
                 checkin_datetime=None,
                 assigned_bed=False):
        attributes = {
            'hmis': hmis,
            'age': age,
            'disability_status': disability_status,
            'veteran': veteran,
            'gender': gender,
            'checkin_datetime': checkin_datetime,
            'assigned_bed': assigned_bed
        }

        super().__init__(attributes)

    @classmethod
    def load(cls, object):
        return cls(**object)

    def check_in(self):
        self.attributes['checkin_datetime'] = datetime.now(tz=pytz.utc).isoformat()


class Administrator(Model):
    def __init__(self, email, password):
        attrs = {
            'email': email,
            'password': password,
            'salt': None  # TODO
        }
        super().__init__(attrs)

    @classmethod
    def load(cls, attrs):
        return cls(**attrs)

