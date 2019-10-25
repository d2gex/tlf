from src import models
from datetime import datetime, timedelta


def test_db_operations():
    arrival_1 = models.Arrivals(expectedArrival=datetime.utcnow() + timedelta(seconds=10), vehicleId='BX54DMZ')
    arrival_2 = models.Arrivals(expectedArrival=datetime.utcnow() + timedelta(seconds=20), vehicleId='BI9999X')
    arrival_3 = models.Arrivals(expectedArrival=datetime.utcnow() + timedelta(seconds=30), vehicleId='JI888hX')

    stop_id = '444450W'
    # Create a record afresh
    models.StopPoint.objects(pk=stop_id).update_one(upsert=True, add_to_set__arrivals=[arrival_1])
    assert len(models.StopPoint.objects().all()) == 1

    # Update the record in place by adding more embedded documents
    models.StopPoint.objects(pk=stop_id).update_one(upsert=True,
                                                    full_result=True,
                                                    add_to_set__arrivals=[arrival_2, arrival_3])

    assert len(models.StopPoint.objects().all()) == 1
    db_data = models.StopPoint.objects().first()
    assert len(db_data.arrivals) == 3
    assert db_data.arrivals[0].vehicleId == 'BX54DMZ'
