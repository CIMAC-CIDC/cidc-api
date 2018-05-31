#!/usr/bin/env python3
"""Unit test file for the ingestion API
"""
from eve.tests import TestBase, TestMinimal
from eve.tests.test_settings import MONGO_DBNAME, MONGO_HOST, MONGO_PASSWORD, MONGO_USERNAME


def test_simple():
    assert len(['a', 'b', 'c']) == 3
