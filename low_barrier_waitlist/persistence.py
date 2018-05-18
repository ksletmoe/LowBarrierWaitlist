from . import mongo
from .models import Participant


def getParticipant(hmisid):
    record = mongo.db.users.find_one({'hmis': str(hmisid)})
    if record:
        return Participant.load(record)
    else:
        return None


def updateParticipant(participant):
    res = mongo.db.users.update_one({'hmis': str(participant.hmis)},
        {'$set': participant.dump()})
    return res.modified_count == 1
