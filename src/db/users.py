import hashlib
from secrets import token_hex
from . import books
from .library_schema import authenticate_user
from .swen344_db_utils import exec_get_all, exec_commit
import json

def register_user(username, password, first_name, middle_name, last_name, email, phone) -> None:
    is_registered = username_exists(username)
    if not is_registered:
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = """
            INSERT INTO library.users (username, password_hash, first_name, middle_name, last_name, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        exec_commit(query, (username, hash, first_name, middle_name, last_name, email, phone))
    data = dict(
        first_name = first_name,
        middle_name = middle_name,
        last_name = last_name,
        email = email,
        phone = phone,
        username = username,
        password = password
    )
    jdata = json.dumps(data)
    return is_registered, jdata

def username_exists(username) -> bool:
    query = """
        SELECT users.username
        FROM library.users
        WHERE username=%s
        """
    result = exec_get_all(query, (username,))
    return (result != [])

def login(username, password) -> int:
    input_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    query = """
        SELECT users.password_hash
        FROM library.users
        WHERE username=%s
        """
    result = exec_get_all(query, (username,))
    try:
        user_password = result[0][0]
        db_hash = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
        session_key = generate_session_key(username) if db_hash == input_hash else None
    except:
        session_key = None

    data = dict(
        username = username,
        password = password,
        session_key = session_key
    )
    jdata = json.dumps(data)

    return session_key, jdata

def generate_session_key(username) -> str:
    session_key = token_hex(16)
    query = """
        UPDATE library.users
        SET session_key=%s
        WHERE users.username=%s;
        """
    exec_commit(query, (session_key, username))
    return session_key

def logout(session_key):
    query = """
        UPDATE library.users
        SET session_key=%s
        WHERE users.session_key=%s;
        """
    exec_commit(query, (None, session_key))
    data = dict(
        session_key = session_key
    )
    jdata = json.dumps(data)
    return jdata

def edit_user_info(query, args) -> bool:
    is_updated = True
    try:
        exec_commit(query, args)
    except:
        is_updated = False
    return is_updated

def change_username(session_key, new_username) -> bool:
    if authenticate_user(session_key):
        query = """
            UPDATE library.users
            SET username=%s
            WHERE users.session_key=%s;
            """
        data = dict(
            username = new_username,
            session_key = session_key
        )
        jdata = json.dumps(data)
        return edit_user_info(query, (session_key, new_username)), jdata

def change_password(session_key, new_password) -> bool:
    query = """
    UPDATE library.users
    SET password=%s
    WHERE users.session_key=%s;
    """
    data = dict(
        password = new_password,
        session_key = session_key
    )
    jdata = json.dumps(data)
    return edit_user_info(query, (session_key, new_password)), jdata

def delete_user(session_key, user_id) -> None:
    is_deleted = False
    if authenticate_user(session_key):
        try:
            query = """
                DELETE FROM library.users
                WHERE users.user_id=%s
                """
            exec_commit(query, (user_id,))
            is_deleted = True
        except:
            pass

    data = dict(
        user_id = user_id
    )
    jdata = json.dumps(data)

    return is_deleted, jdata

def get_all(session_key) -> json:
    data = []

    if authenticate_user(session_key):
        query = """
            SELECT users.user_id, users.first_name, users.middle_name, users.last_name
            FROM library.users
            """
        result = exec_get_all(query, )
        columns = ["user id", "first name", "middle name", "last name"]

        for book in result:
            location = []
            for i in range(len(columns)):
                location.append((columns[i], book[i]))
            data.append(dict(location))

    jdata = json.dumps(data)
    return jdata

def get_checkouts(session_key) -> list:
    data = []

    if authenticate_user(session_key):
        query = """
                SELECT books.title, checked_out.borrowed_date, locations.title, book_copies.book_copy_id
                FROM library.checked_out
                INNER JOIN library.users USING (user_id)
                INNER JOIN library.book_copies USING (book_copy_id)
                INNER JOIN library.books USING (book_id)
                INNER JOIN library.locations USING (location_id)
                WHERE users.session_key=%s
                ORDER BY books.title ASC
                """

        result = exec_get_all(query, (session_key,))
        columns = ["title", "borrow date", "location", "copy id"]
        
        for book in result:
            location = []
            for i in range(len(columns)):
                location.append((columns[i], book[i]))
            data.append(dict(location))

    jdata = json.dumps(data, default=str)
    return jdata

"""
Given a book_id it searches for available copies. If there are copies available
a message is returned saying that the book cannot be reserved. Else a reserve
record is created in library.reserved
"""
def reserve_book(session_key, book_id) -> None:
    result = books.search_for_available_book_copies(book_id)
    num_of_available_copies = len(result)
    is_reservable = ( num_of_available_copies < 1 )
    is_logged_in = authenticate_user(session_key)

    if is_reservable and is_logged_in:
        query = """
            INSERT INTO library.reserved (user_id, book_id)
            VALUES (
                (SELECT users.user_id FROM library.users
                WHERE users.session_key=%s),
                %s
            )
            """
        exec_commit(query, (session_key,book_id))

    data = dict(
        session_key = session_key,
        book_id = book_id
    )
    jdata = json.dumps(data, default=str)

    return (is_reservable and is_logged_in), jdata

"""
If the book copy is not already checked out, a record is created in library.checked_out
"""
def checkout_book(session_key, book_copy_id, current_date) -> bool:
    book_is_avaliable = not books.is_checked_out(book_copy_id)
    if book_is_avaliable and authenticate_user(session_key):
        query = """
            INSERT INTO library.checked_out (user_id, book_copy_id, borrowed_date)
            VALUES
            (
                SELECT users.user_id FROM library.users
                WHERE users.session_key=%s
            ), %s, %s);
            
            UPDATE library.book_copies
            SET is_checked_out = true
            WHERE book_copies.book_copy_id=%s
            """
        exec_commit(query, (session_key, book_copy_id, current_date, book_copy_id))

    data = dict(
        session_key = session_key,
        book_copy_id = book_copy_id,
        current_date = current_date
    )
    jdata = json.dumps(data, default=str)

    return book_is_avaliable, jdata

"""
Updates the checked_out record associated with the given id
with the date returned and updates the book copies with 
the given id to is_checked_out = false
"""
def return_book(session_key, return_date, checked_out_id, book_copy_id) -> None:
    is_returned = False
    if authenticate_user(session_key):
        try:
            query = """
                UPDATE library.checked_out
                SET returned_date=%s
                WHERE checked_out.checked_out_id=%s;
                UPDATE library.book_copies
                SET is_checked_out = false
                WHERE book_copies.book_copy_id=%s
                """
            exec_commit(query, (return_date, checked_out_id, book_copy_id))
            days_borrowed = books.get_days_borrowed_after_returned(checked_out_id)
            books.update_fee(days_borrowed, checked_out_id)
            is_returned = True
        except:
            pass

    data = dict(
        return_date = return_date,
        checked_out_id = checked_out_id,
        book_copy_id = book_copy_id
    )
    jdata = json.dumps(data, default=str)

    return is_returned, jdata
