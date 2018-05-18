#from low_barrier_waitlist.importer.data_importer import DataImporter
from data_importer import DataImporter
from low_barrier_waitlist.ranker import Ranker
import low_barrier_waitlist.persistence
from pymongo import MongoClient

import sys

if __name__ == '__main__':
    importer = DataImporter()
    importer.parse_input_file(sys.argv[1])
    participants = importer.get_participants()
    client = MongoClient()
    db = client.low_barrier_waitlist
    for p in participants:
        print(p.dump())
        res = db.users.update_one({'hmis': str(p.hmis)},
                                  {'$set': p.attributes},
                                  upsert=True)

    print(len(participants))

    # get top 40
    r = Ranker(participants)
    for rp in r.ranked_participants[:200:]:
        print("ID: {} (Rank: {} [age: {}, vet: {}, dis: {})".format(rp.participant.hmis, rp.rank, rp.participant.age,
                                                              rp.participant.veteran, rp.participant.disability_status))

