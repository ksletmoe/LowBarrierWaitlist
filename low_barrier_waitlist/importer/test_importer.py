#from low_barrier_waitlist.importer.data_importer import DataImporter
from data_importer import DataImporter


import sys

if __name__ == '__main__':
    importer = DataImporter()
    importer.parse_input_file(sys.argv[1])
    participants = importer.get_participants()
    for p in participants:
        print(p.dump())
    print(len(participants))

