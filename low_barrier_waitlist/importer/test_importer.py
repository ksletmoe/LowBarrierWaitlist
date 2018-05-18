from data_importer import DataImporter
from low_barrier_waitlist.ranker import Ranker
from pymongo import MongoClient

import sys

if __name__ == '__main__':
    importer = DataImporter()
    importer.parse_input_file(sys.argv[1])
    participants = importer.get_participants()
    client = MongoClient()
    db = client.low_barrier_waitlist
    for p in participants:
        #print(p.dump())
        low_barrier_waitlist.persistence.update_participant(db, p, low_barrier_waitlist.persistence.get_import_attributes())

    print(len(participants))

    # get top 40
    r = Ranker(participants)
    for rp in r.ranked_participants[:200:]:
        print("ID: {} (Rank: {} [age: {}, vet: {}, dis: {})".format(rp.participant.hmis, rp.rank, rp.participant.age,
                                                              rp.participant.veteran, rp.participant.disability_status))

