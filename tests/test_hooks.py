"""
Tests for the functions in hooks.py
"""
from unittest.mock import patch
from hooks import log_user_create, serialize_objectids


def test_log_user_create():
    """
    Test log_user_create.
    """
    assert not log_user_create([{"a": "b"}])


def test_serialize_objectids():
    """
    Test serialize_objectids.
    """
    items = [{"assay": b"1234567890AB", "trial": b"BA0987654321", "file_name": "file1"}]
    assert not serialize_objectids(items)
