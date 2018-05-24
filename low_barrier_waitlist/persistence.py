from .models import Participant, Administrator
import datetime
from .ranker import Ranker
import pymongo


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


def get_recent_participants(db_client, limit=100):
    td = datetime.timedelta(weeks=1)
    one_week_ago = datetime.date.today() - td
    min_checkin_time = datetime.datetime.combine(
                one_week_ago,
                datetime.datetime.min.time())
    records = db_client.users.find(
        {
            "checkin_datetime": {"$ne": None, "$gt": min_checkin_time},
            "assigned_bed": {"$ne": True}
        }
    ).sort("checkin_datetime", pymongo.ASCENDING).limit(limit)

    participants = []
    for r in records:
        print(r)
        r.pop('_id', None)
        participants.append(Participant.load(r))
    r = Ranker(participants)

    return r.ranked_participants


def get_administrator(db_client, email):
    record = db_client.administrators.find_one({'email': email})
    if record:
        return Administrator.load(record)
    else:
        return None


def update_administrator(db_client, administrator):
    res = db_client.administrators.update_one({'email': administrator.email},
                                              {'$set': administrator.dump()})

    return res.modified_count == 1


def update_participant(db_client, participant, attr_names=[]):
    update_attr = participant.attributes
    if attr_names:
        update_attr = {k: v for k, v in participant.attributes.items() if k in attr_names}
    res = db_client.users.update_one({'hmis': str(participant.hmis)},
                                     {'$set': update_attr},
                                     upsert=True)
    return res.modified_count == 1
