#from low_barrier_waitlist.importer.data_importer import DataImporter
from data_importer import DataImporter
from low_barrier_waitlist.ranker import Ranker

import sys

if __name__ == '__main__':
    importer = DataImporter()
    importer.parse_input_file(sys.argv[1])
    participants = importer.get_participants()
    for p in participants:
        print(p.dump())
    print(len(participants))

    # get top 40
    r = Ranker(participants)
    for rp in r.ranked_participants[:40:]:
        print("ID: {} (Rank: {} [age: {}, vet: {}, dis: {})".format(rp.participant.hmis, rp.rank, rp.participant.age,
                                                              rp.participant.veteran, rp.participant.disability_status))

