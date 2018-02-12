#!/usr/bin/env python3
"""Unit test file for the ingestion API
"""


from eve.tests import TestBase, TestMinimal
from eve.tests.test_settings import MONGO_DBNAME, MONGO_HOST, MONGO_PASSWORD, MONGO_USERNAME
from ingestion_api import app


class TestIngestionApi(TestMinimal):
    """[summary]
    """

    def setUp(self, settings_file=None, url_converters=None):
        """Sets up the EVE application with settings appropriate to testing

        Keyword Arguments:
            settings_file {[type]} -- [description] (default: {None})
            url_converters {[type]} -- [description] (default: {None})
        """
        self.app = app
        self.test_client = app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['MONGO_HOST'] = 'localhost'
        self.app.config['MONGO_USERNAME'] = ""
        self.app.config['MONGO_PASSWORD'] = ""

    def test_post(self):
        """[summary]
        """
        message = {"message": "hi"}
        r, status_code = self.post('test', message)
        self.assert201(status_code)
