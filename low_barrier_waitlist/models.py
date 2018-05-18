import json


class Model:
    def __init__(self, attributes):
        self.attributes = attributes

    def dump(self):
        return json.dumps(self.attributes)

    def __getattribute__(self, name):
        return self.attributes.get(name)

    def load(self, object):
        raise NotImplementedError('Implement in child model')


class Participant(Model):
    def __init__(self,
                 hmis,
                 age,
                 disability_status,
                 veteran,
                 checkin_datetime,
                 assigned_bed):
        attributes = {
            'hmis': hmis,
            'age': age,
            'disability_status': disability_status,
            'veteran': veteran,
            'checkin_datetime': checkin_datetime,
            'assigned_bed': assigned_bed
        }

        super().__init__(attributes)

    @classmethod
    def load(cls, object):
        return cls(**object)


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

