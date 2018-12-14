"""Unit test file for the ingestion API
"""
import unittest
from eve import Eve
from ingestion_api import BearerAuth, configure_logging
import hooks


def add_hooks(app: Eve):
    """[summary]
    
    Arguments:
        app {Eve} -- [description]
    """
    # Accounts hooks
    app.on_inserted_accounts += hooks.log_user_create
    app.on_updated_accounts += hooks.log_user_modified
    app.on_inserted_accounts_info += hooks.log_user_create
    app.on_updated_accounts_update += hooks.log_user_modified

    # Ingestion Hooks
    app.on_updated_ingestion += hooks.process_data_upload
    app.on_insert_ingestion += hooks.register_upload_job

    # Data Hooks
    app.on_insert_data += hooks.serialize_objectids
    app.on_inserted_data += hooks.check_for_analysis
    app.on_updated_data += hooks.data_patched
    app.on_inserted_data_edit += hooks.check_for_analysis
    app.on_insert_data_edit += hooks.serialize_objectids
    app.on_update_data_vis += hooks.user_visibility_toggle

    # Analysis Hooks
    app.on_insert_analysis += hooks.register_analysis

    # Pre get filter hook.
    app.on_pre_GET += hooks.filter_on_id

    # Logging request related hooks
    app.on_post_PATCH += hooks.log_patch_request
    app.on_post_POST += hooks.log_post_request
    app.on_post_DELETE += hooks.log_delete_request


class TestAPICalls(unittest.TestCase):
    """[summary]

    Arguments:
        unittest {[type]} -- [description]
    """

    def setUp(self):
        self.app = Eve("ingestion_api", auth=BearerAuth, settings="./settings.py")
        self.app.debug = True
        add_hooks(self.app)
        configure_logging()
        self.app.run(host="0.0.0.0", port=8400)

    def tearDown(self):
        self.app = None


def test_simple():
    assert len(["a", "b", "c"]) == 3
