import unittest
from tests.test_utils import *
from src.db import library_schema

class TestLibraryDB(unittest.TestCase):

    def test_rebuild_tables(self):
        """Rebuild the tables"""
        library_schema.rebuild_tables()
        assert_sql_count(self, "SELECT * FROM library.books", 0)

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        library_schema.rebuild_tables()
        library_schema.rebuild_tables()
        assert_sql_count(self, "SELECT * FROM library.books", 0)

    def test_seed_data_works(self):
        """Attempt to insert the seed data"""
        library_schema.rebuild_tables()
        library_schema.populate_tables('tests/data/full_library.sql')
        assert_sql_count(self, "SELECT * FROM library.books", 6)

    if __name__ == '__main__':
        unittest.main()