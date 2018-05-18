# Reads a csv file uploaded by TP admins and extracts the participant info

import csv
from datetime import datetime, timedelta

class DataImporter:

    def __init__(self):
        self.participants = dict()
        self.field_mappings = {
            'ClientID':
                {
                    'field_name': 'client_id',
                    'transform': (lambda x: x)
                },
            'Age':
                {
                    'field_name': 'age',
                    'transform': (lambda x: x)
                },
            'U.S. Military Veteran?':
                {
                    'field_name': 'is_veteran',
                    'transform': (lambda x: True if x.strip() in ('YES', 'yes', 'Y', 'y') else False)
                },
            'Does the client have a disabling condition?':
                {
                    'field_name': 'has_disability',
                    'transform': (lambda x: True if x.strip().startswith in ('YES', 'yes', 'Y', 'y') else False)
                },
            'Gender':
                {
                    'field_name': 'gender',
                    'transform': (lambda x: x.strip().upper())
                },
            'Waitlist Event Date':
                {
                    'field_name': 'event_date',
                    'transform': (lambda x: datetime.strptime(x.strip(), '%m/%d/%Y'))
                },
            'AM / PM':
                {
                    'field_name': 'event_hour_offset',
                    'transform': (lambda x: 12 if x.strip().upper() == 'PM' else 0)
                },
            'Hour':
                {
                    'field_name': 'event_hour',
                    'transform': (lambda x: int(x) if x else 0)
                },
            'Minute':
                {
                    'field_name': 'event_minute',
                    'transform': (lambda x: int(x) if x else 0)
                }
        }
        self.export_fields = ['client_id', 'age', 'is_veteran', 'has_disability', 'gender']

    def parse_input_file(self, filename):
        with open(filename, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #print(csv_reader.fieldnames)
            try:
                for row in csv_reader:
                    self.process_row(row)

            except csv.Error as e:
                #TODO convert to log
                print('Parsing error in file {}, line {}: {}'.format(filename, csv_reader.line_num, e))
                return False
        return True


    def process_row(self, row):
        #print(row)
        event = dict()
        for csv_field, csv_value in row.items():
            mapping = self.field_mappings.get(csv_field, None)
            if mapping:
                event[mapping['field_name']] = mapping['transform'](csv_value)
        #print(event)
        event['event_date'] += timedelta(hours=event['event_hour_offset']+event['event_hour'])
        event['event_date'] += timedelta(hours=event['event_minute'])

        if event['client_id'] in self.participants:
            if self.participants[event['client_id']]['event_date'] < event['event_date']:
                self.participants[event['client_id']] = event
        else:
            self.participants[event['client_id']] = event

    def get_participants(self):
        return { x: {k: v for k, v in y.items() if k in self.export_fields} for x,y in self.participants.items() }
