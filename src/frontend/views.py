import json
from datetime import datetime

from collections import defaultdict
from src import utils
from src import models
from flask import Blueprint, render_template, abort

frontend = Blueprint('frontend', __name__, static_folder='../static/frontend')


@frontend.route('/<string:stop_point_id>', methods=['GET'])
def get_stop_point_info(stop_point_id):
    response = utils.call_api(utils.API_END_POINT_TEMPLATE.format(stop_point_id))
    api_data = response.text
    if response.status_code == 404:
        abort(404)
    try:
        data = json.loads(api_data)
    except json.decoder.JSONDecodeError:
        abort(500)

    arrivals = [models.Arrivals(expectedArrival=datetime.strptime(each_arrival['expectedArrival'][:-1], '%Y-%m-%dT%H:%M:%S'),
                                vehicleId=each_arrival['vehicleId'])
                for each_arrival in data]
    if arrivals:
        models.StopPoint.objects(pk=stop_point_id).update_one(upsert=True,
                                                              add_to_set__arrivals=arrivals)
    else:
        api_data = "No data available at this time"
    return render_template('frontend/api_data.html', data=api_data)


@frontend.route('/history/<string:stop_point_id>', methods=['GET'])
def get_history(stop_point_id):
    db_data = models.StopPoint.objects(pk=stop_point_id).first()
    if not db_data:
        abort(404)
    data = defaultdict(list)
    for arrival in db_data.arrivals:
        data[arrival.vehicleId].append({'expectedArrival': arrival.expectedArrival,
                                        'timestamp': arrival.local_timestamp})
    return render_template('frontend/history.html', data=data)


@frontend.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404


@frontend.app_errorhandler(500)
def handle_404(err):
    return render_template('500.html'), 500
