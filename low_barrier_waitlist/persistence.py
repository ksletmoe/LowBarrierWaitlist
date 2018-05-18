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
        record.pop('_id', None)
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
    update_attr = participant.attributes
    if attr_names:
        update_attr = {k: v for k, v in participant.attributes.items() if k in attr_names}
    print(update_attr)
    res = db_client.users.update_one({'hmis': str(participant.hmis)},
                                     {'$set': update_attr},
                                     upsert=True)
    print(res)
    return res.modified_count == 1
