from . import mongo
from .models import Participant, Administrator


def get_participant(hmisid):
    record = mongo.db.users.find_one({'hmis': str(hmisid)})
    if record:
        return Participant.load(record)
    else:
        return None


def update_participant(participant):
    res = mongo.db.users.update_one({'hmis': str(participant.hmis)},
                                    {'$set': participant.dump()})
    return res.modified_count == 1


def get_administrator(email):
    record = mongo.db.administrators.find_one({'email': email})
    if record:
        return Administrator.load(record)
    else:
        return None


def update_administrator(administrator):
    res = mongo.db.administrators.update_one({'email': administrator.email},
                                             {'$set': administrator.dump()})

    return res.modified_count == 1
