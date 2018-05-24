# Reads a csv file uploaded by TP admins and extracts the participant info

from low_barrier_waitlist.models import Participant
import csv
from datetime import datetime, timedelta


class DataImporter:

    def __init__(self):
        self.participants = dict()
        self.field_mappings = {
            "ClientID": {
                "field_name": "client_id",
                "transform": (lambda x: x),
            },
            "Age": {"field_name": "age", "transform": (lambda x: int(x))},
            "U.S. Military Veteran?": {
                "field_name": "is_veteran",
                "transform": (
                    lambda x: True
                    if x.strip().upper().startswith("Y")
                    else False
                ),
            },
            "Does the client have a disabling condition?": {
                "field_name": "has_disability",
                "transform": (
                    lambda x: True
                    if x.strip().upper().startswith("Y")
                    else False
                ),
            },
            "Gender": {
                "field_name": "gender",
                "transform": (lambda x: x.strip().upper()),
            },
            "Waitlist Event Date": {
                "field_name": "event_date",
                "transform": (
                    lambda x: datetime.strptime(x.strip(), "%m/%d/%Y")
                ),
            },
            "AM / PM": {
                "field_name": "event_hour_offset",
                "transform": (
                    lambda x: 12 if x.strip().upper() == "PM" else 0
                ),
            },
            "Hour": {
                "field_name": "event_hour",
                "transform": (lambda x: int(x) if x else 0),
            },
            "Minute": {
                "field_name": "event_minute",
                "transform": (lambda x: int(x) if x else 0),
            },
        }

    def parse_input_file(self, filename):
        with open(filename, "r", newline="") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            try:
                for row in csv_reader:
                    self.process_row(row)

            except csv.Error:
                return False
        return True

    def process_row(self, row):
        event = dict()
        for csv_field, csv_value in row.items():
            mapping = self.field_mappings.get(csv_field, None)
            if mapping:
                event[mapping["field_name"]] = mapping["transform"](csv_value)

        event["event_date"] += timedelta(
            hours=event["event_hour_offset"] + event["event_hour"]
        )
        event["event_date"] += timedelta(hours=event["event_minute"])

        if event["client_id"] in self.participants:
            if (
                self.participants[event["client_id"]]["event_date"]
                < event["event_date"]
            ):
                self.participants[event["client_id"]] = event
        else:
            self.participants[event["client_id"]] = event

    def get_participants(self):
        return [
            Participant(
                v["client_id"],
                v["age"],
                v["has_disability"],
                v["is_veteran"],
                v["gender"],
                None,
                None,
            )
            for k, v in self.participants.items()
        ]
