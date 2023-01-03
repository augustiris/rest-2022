import json
import unittest

from tests.test_utils import *
from src.db import library_schema, users

class TestCrud(unittest.TestCase):

    def setUp(self):
        library_schema.rebuild_tables()
        library_schema.populate_tables("tests/data/full_library.sql")

    def test_add_user(self):
        data = dict(
            first_name = 'Ada',
            middle_name = 'Mary',
            last_name = 'Lovelace',
            email = 'Lovelace@gmail.com',
            phone = '020-321-1029',
            username = 'ada123',
            password = '12345'
        )

        jdata = json.dumps(data)
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}

        result = post_rest_call(self, 'http://localhost:5000/users/create', jdata, hdr)
        print(f"Add-User_BodyParams:{result}")

    def test_remove_user(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}
        
        result = delete_rest_call(self, 'http://localhost:5000/users/delete/1', hdr)
        print(f"Delete-User_Response:{result}")

    def test_user_checkouts(self):
        s_key = users.login('ada123', '12345')[0]
        hdr = {'content-type': 'application/json',
            'session': s_key}

        library_schema.populate_tables("tests/data/checkouts.sql")
        result = get_rest_call(self, 'http://localhost:5000/users/checkouts', {}, hdr)
        print(f"User-Checkouts_Response:{result}")
