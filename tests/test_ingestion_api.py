"""Unit test file for the ingestion API
"""
import unittest
from settings import DOMAIN


class TestAPICalls(unittest.TestCase):
    """[summary]

    Arguments:
        unittest {[type]} -- [description]
    """

    def test_schemas_item_rules(self):
        """
        Test schemas for having keys related to item rules.
        """
        expected_fields = [
            "public_methods",
            "resource_methods",
            "allowed_item_roles",
            "schema"
        ]
        for key, value in DOMAIN.items():
            if key not in ["data/query", "status", "data_edit"]:
                with self.subTest():
                    self.assertTrue(all([field in value for field in expected_fields]))
