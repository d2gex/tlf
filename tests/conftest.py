import pytest
import json

from os.path import join
from src.app import create_app, db
from src import models
from tests import config as test_config
from tests import utils as test_utils


@pytest.fixture(scope='session')
def api_data():
    with open(join(test_utils.TEST, 'stubs', 'api_data.json')) as fh:
        content = fh.read()
    return content


@pytest.fixture(scope='session', autouse=True)
def test_db_authenticate_once():
    app = create_app(config_class=test_config.TestingConfig)
    with app.app_context():
        models.StopPoint.objects.first()  # It will authenticate this execution thread once against the MongoDB


@pytest.fixture(autouse=True)
def reset_database_tear_up_down():
    '''Drop the database at the beginning and end of each module. It requires that this running thread had already
    being authenticated
    '''
    app = create_app(config_class=test_config.TestingConfig)
    with app.app_context():  # the context needs to be pushed as Flask MongoEngine is using current_app
        db.connection.drop_database(test_config.TestingConfig.MONGODB_SETTINGS['db'])
    yield


@pytest.fixture
def frontend_app():
    app = create_app(config_class=test_config.TestingConfig)
    frontend = app.test_client(use_cookies=True)
    return frontend
