import json
from re import S
import unittest

from tests.test_utils import *
from src.db import library_schema, users

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        library_schema.rebuild_tables()

    def test(self):
        print(users.login('ada123', '12345'))

    def test_login(self):
        library_schema.populate_tables("tests/data/users.sql")
        data = dict(
            username = 'ada123',
            password = '12345'
        )

        jdata = json.dumps(data)
        hdr = {'content-type': 'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users/login', jdata, hdr)
        print(f"Login_BodyParams:{result}")

    def test_authenticate_user(self):
        library_schema.populate_tables("tests/data/users.sql")
        s_key = users.login('ada123','12345')[0]
        result = users.authenticate_user(s_key)
        self.assertTrue(result)

    def test_change_username(self):
        library_schema.populate_tables("tests/data/users.sql")
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}

        data = dict(
            new_username = 'ada777'
        )
        jdata = json.dumps(data)
    
        result = put_rest_call(self, 'http://localhost:5000/users/edit-username', jdata, hdr)
        print(f"Edit-Username_BodyParams:{result}")
    
    def test_change_password(self):
        library_schema.populate_tables("tests/data/users.sql")
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}

        data = dict(
            new_password = 'slghas;oerwhw4r'
        )
        jdata = json.dumps(data)
        result = put_rest_call(self, 'http://localhost:5000/users/change-password', jdata, hdr)
        print(f"Change-Password_BodyParams:{result}")

    def test_borrow_book(self):
        library_schema.populate_tables("tests/data/full_library.sql")
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        
        data = dict(
            user_id = '1',
            book_copy_id = '1',
            current_date = '2022-10-20'
        )

        jdata = json.dumps(data)
        result = post_rest_call(self, 'http://localhost:5000/users/borrow-book',
            jdata, hdr)
        print(f"Borrow-Book_BodyParams:{result}")

    def test_reserve_book(self):
        library_schema.populate_tables("tests/data/full_library.sql")
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        
        data = dict(
            user_id = '1',
            book_id = '1'
        )

        jdata = json.dumps(data)
        result = post_rest_call(self, 'http://localhost:5000/users/reserve-book',
            jdata, hdr)
        print(f"Reserve-Book_BodyParams:{result}")

    def test_return_book(self):
        library_schema.populate_tables("tests/data/full_library.sql")
        library_schema.populate_tables("tests/data/checkouts.sql")

        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}

        data = dict(
            return_date = '2000-20-21',
            checked_out_id = '1',
            book_copy_id = '1'
        )
        jdata = json.dumps(data)
        result = put_rest_call(self, 'http://localhost:5000/books/return-book', jdata, hdr)
        print(f"Return-Book_BodyParams:{result}")
