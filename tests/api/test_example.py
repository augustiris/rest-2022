import unittest
from tests.test_utils import *
from src.db.example import rebuild_tables

class TestExample(unittest.TestCase):

    def setUp(self):
        rebuild_tables()
        insert_test_data('tests/data/example.sql')

    def test_hello_world(self):
        expected = { '1' : 'hello, world!' }
        actual = get_rest_call(self, 'http://localhost:5000/hello-world')
        self.assertEqual(expected, actual)
