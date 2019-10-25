from src.app import db
from datetime import datetime


class Arrivals(db.EmbeddedDocument):
    vehicleId = db.StringField(max_length=15, required=True)
    expectedArrival = db.DateTimeField(required=True)
    local_timestamp = db.DateTimeField(default=datetime.utcnow)


class StopPoint(db.Document):
    id = db.StringField(max_length=20, primary_key=True)
    # UTC-offset in which time is stored given that Mongo stores datetimes in UTC
    utc_arrival_timezone = db.IntField(default=0)
    arrivals = db.EmbeddedDocumentListField(Arrivals)

