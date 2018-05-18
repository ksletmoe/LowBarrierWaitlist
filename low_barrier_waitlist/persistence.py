from .models import Participant, Administrator


def get_import_attributes():
    return ['hmis', 'age', 'disability_status', 'veteran', 'gender']


def get_checkin_attributes():
    return ['hmis', 'checkin_datetime']


def get_assign_bed_attributes():
    return ['hmis', 'assigned_bed']


def get_participant(db_client, hmisid):
    record = db_client.users.find_one({'hmis': str(hmisid)})
    if record:
        return Participant.load(record)
    else:
        return None


def get_administrator(db_client, email):
    record = db_client.administrators.find_one({'email': email})
    if record:
        return Administrator.load(record)
    else:
        return None


def update_administrator(db_client, administrator):
    res = db_client.administrators.update_one({'email': administrator.email},
                                             {'$set': administrator.dump()})


def update_participant(db_client, participant, attr_names=[]):
    if attr_names:
        res = db_client.users.update_one({'hmis': str(participant.hmis)},
            {'$set': {k: v for k,v in participant.attributes.items() if k in attr_names}},
            upsert=True)
    else:
        res = db_client.users.update_one({'hmis': str(participant.hmis)},
            {'$set': participant.attributes},
            upsert=True)
    return res.modified_count == 1
