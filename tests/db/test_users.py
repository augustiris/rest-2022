from atexit import register
import unittest
from src.db import users
from src.db.swen344_db_utils import exec_get_all
from src.db.users import logout, register_user, username_exists, login
from tests.test_utils import *
from src.db import library_schema

class TestUsers(unittest.TestCase):

    def setUp(self):
        library_schema.rebuild_tables()

    def test_register_user_pass(self):
        result = register_user('John123', 'securepassword', 'John',
            'Smith', 'Jones', 'smith@gmail.com', '705-543-6543')
        self.assertTrue(not result[0])

    def test_register_duplicate_username(self):
        register_user('John123', 'securepassword', 'John',
            'Smith', 'Jones', 'smith@gmail.com', '705-543-6543')
        result = register_user('John123', 'verysecurepassword', 'Johnny',
            'Ron', 'Wood', 'smithy@gmail.com', '705-333-6543')
        self.assertTrue(result[0])

    def test_username_exists_true(self):
        library_schema.populate_tables("tests/data/full_library.sql")
        expected = True
        actual = username_exists('ada123')
        self.assertEqual(expected, actual)

    def test_username_exists_false(self):
        library_schema.populate_tables("tests/data/full_library.sql")
        expected = False
        actual = username_exists('not a username')
        self.assertEqual(expected, actual)

    def test_get_checkouts(self):
        library_schema.populate_tables("tests/data/full_library.sql")
        library_schema.populate_tables("tests/data/checkouts.sql")
        s_key = users.login('ada123', '12345')[0]
        result = users.get_checkouts(s_key)
        print('checkouts:' + result[0])

    if __name__ == '__main__':
        unittest.main()