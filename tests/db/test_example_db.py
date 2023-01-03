import unittest
from src.db.example import *
from src.db.swen344_db_utils import connect
from tests.test_utils import *

class TestExampleDBSchema(unittest.TestCase):

    def test_rebuild_tables(self):
        """Rebuild the tables"""
        rebuild_tables()
        assert_sql_count(self, "SELECT * FROM example_table", 0)

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        rebuild_tables()
        rebuild_tables()
        assert_sql_count(self, "SELECT * FROM example_table", 0)

    def test_seed_data_works(self):
        """Attempt to insert the seed data"""
        rebuild_tables()
        insert_test_data('tests/data/example.sql')
        assert_sql_count(self, "SELECT * FROM example_table", 1)