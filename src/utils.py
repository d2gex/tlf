import requests

API_END_POINT_TEMPLATE = "https://api.tfl.gov.uk/StopPoint/{}/arrivals"


def call_api(endpoint):
    return requests.get(endpoint)
