import json

from src import models
from unittest.mock import patch


def test_404_error(frontend_app):

    not_found_stop_point = 444
    with patch('src.utils.call_api') as mock_api_call:
        mock_api_call.return_value.status_code = 404
        response = frontend_app.get(f'/frontend/{not_found_stop_point}', follow_redirects=True)
    assert response.status_code == 404


def test_500_error(frontend_app):

    not_found_stop_point = 444
    with patch('src.utils.call_api') as mock_api_call:
        mock_api_call.return_value.status_code = 200
        mock_api_call.return_value.text = 'No json'
        response = frontend_app.get(f'/frontend/{not_found_stop_point}', follow_redirects=True)
    assert response.status_code == 500


def test_200_no_data_available(frontend_app):

    not_found_stop_point = 444
    with patch('src.utils.call_api') as mock_api_call:
        mock_api_call.return_value.status_code = 200
        mock_api_call.return_value.text = '[]'
        response = frontend_app.get(f'/frontend/{not_found_stop_point}', follow_redirects=True)
    assert response.status_code == 200
    assert 'No data available at this time' in response.get_data(as_text=True)


def test_200_successful_call(frontend_app, api_data):

    not_found_stop_point = 444
    with patch('src.utils.call_api') as mock_api_call:
        mock_api_call.return_value.status_code = 200
        mock_api_call.return_value.text = api_data
        response = frontend_app.get(f'/frontend/{not_found_stop_point}', follow_redirects=True)
    assert response.status_code == 200
    assert all(html_elements in response.get_data(as_text=True)
               for html_elements in ('<pre>', 'naptanId', 'expectedArrival'))
    assert len(models.StopPoint.objects().all()) == 1
