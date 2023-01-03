from flask_restful import Resource
from db import users, authors, books
import json

class Library(Resource):

    def add_user(username, password, first_name, middle_name, last_name, email, phone) -> bool:
        return users.register_user(username, password, first_name, middle_name, last_name, email, phone)

    def login(username, password):
        return users.login(username, password)

    def logout(session_key):
        return users.logout(session_key)

    def get_all_users(session_key) -> json:
        return users.get_all(session_key)

    def get_all_books(session_key) -> json:
        return books.get_all(session_key)

    def get_all_authors(session_key) -> json:
        return authors.get_all(session_key)

    def search_by_author_id(session_key, id) -> json:
        return authors.wrote(session_key, id)

    def search_by_genre(session_key, genre) -> json:
        return books.search_by_genre(session_key, genre)

    def list_all_checkouts(session_key) -> json:
        return users.get_checkouts(session_key)

    def change_username(session_key, new_username) -> bool:
        return users.change_username(session_key, new_username)

    def change_password(session_key, new_password) -> bool:
        return users.change_password(session_key, new_password)

    def remove_user(session_key, user_id) -> bool:
        return users.delete_user(session_key, user_id)

    def checkout_book(session_key, book_copy_id, current_date) -> bool:
        return users.checkout_book(session_key, book_copy_id, current_date)

    def return_book(session_key, return_date, checked_out_id, book_copy_id) -> bool:
        return users.return_book(session_key, return_date, checked_out_id, book_copy_id)

    def reserve_book(session_key, book_id) -> bool:
        return users.reserve_book(session_key, book_id)