import unittest
from tests.test_utils import *
from src.db import library_schema, users

class TestLibrary(unittest.TestCase):

    def setUp(self):
        library_schema.rebuild_tables()
        library_schema.populate_tables("tests/data/full_library.sql")

    def test_get_all_users(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        expected = 4
        actual = get_rest_call(self, 'http://localhost:5000/users', {}, hdr)
        self.assertEqual(expected, len(actual))

    def test_get_all_books(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        expected = 9
        actual = get_rest_call(self, 'http://localhost:5000/books', {}, hdr)
        self.assertEqual(expected, len(actual))

    def test_get_all_authors(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        expected = 6
        actual = get_rest_call(self, 'http://localhost:5000/authors', {}, hdr)
        self.assertEqual(expected, len(actual))

    def test_get_fiction(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        expected = 5
        genre = "fICtiON"
        actual = get_rest_call(self, 'http://localhost:5000/books/genre/' + genre, {}, hdr)
        self.assertEqual(expected, len(actual))

    def test_get_non_fiction(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        expected = 1
        genre = "noN-fICtiOn"
        actual = get_rest_call(self, 'http://localhost:5000/books/genre/' + genre, {}, hdr)
        self.assertEqual(expected, len(actual))

    def test_get_non_existent_genre(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        expected = 0
        genre = "not a genre"
        actual = get_rest_call(self, 'http://localhost:5000/books/genre/' + genre, {}, hdr)
        self.assertEqual(expected, len(actual))

    def test_list_books_by_author_id(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        expected = 1
        author_id = "1"
        actual = get_rest_call(self, 'http://localhost:5000/books/author/' + author_id, {}, hdr)
        self.assertEqual(expected, len(actual))

    def test_non_existent_author(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        expected = 0
        author_id = "-1"
        actual = get_rest_call(self, 'http://localhost:5000/books/author/' + author_id, {}, hdr)
        self.assertEqual(expected, len(actual))
        