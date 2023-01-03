from .swen344_db_utils import exec_get_all
from .library_schema import authenticate_user
import json

ONE_WEEK = 7

def get_all(session_key) -> json:
    data = []
    if authenticate_user(session_key):
        query = """
        SELECT books.title, books.genre, books.sub_genre, books.summary, books.publish_date,
            ARRAY_AGG (
                DISTINCT CONCAT(authors.first_name || ' ' || authors.last_name)
            ) author_list,
            locations.title,
            COUNT(book_copies.book_copy_id)

        FROM library.books
        INNER JOIN library.wrote USING (book_id)
        INNER JOIN library.authors USING (author_id)
        INNER JOIN library.book_copies USING (book_id)
        INNER JOIN library.locations USING (location_id)
        GROUP BY books.title, books.genre, books.sub_genre, books.summary, books.publish_date, locations.location_id
        ORDER BY books.title DESC
        """

        result = exec_get_all(query, )
        columns = ["title", "genre", "sub genre", "summary", "publish date", "authors", "location", "copies"]

        for book in result:
            location = []
            for i in range(len(columns)):
                location.append((columns[i], book[i]))
            data.append(dict(location))

    jdata = json.dumps(data, default=str)
    return jdata 

def search_by_genre(session_key, genre) -> json:
    data =[]
    if authenticate_user(session_key):
        genre = genre.capitalize()
        query = """
            SELECT books.title FROM library.books
            WHERE books.genre=%s
            """
        result = exec_get_all(query, (genre, ))
        columns = ["title"]
        for book in result:
            location = []
            for i in range(len(columns)):
                location.append((columns[i], book[i]))
            data.append(dict(location))

    jdata = json.dumps(data)
    return jdata

"""
Given a book_id returns a list of all book copies not
checked out
"""
def search_for_available_book_copies(book_id) -> list:
    query = """
    SELECT book_copies.book_copy_id,
    (
        (SELECT COUNT(book_copies.book_id)
        FROM library.book_copies
        WHERE book_id=%s
        )
        -
        (SELECT COUNT(book_copies.book_id)
        FROM library.book_copies
        WHERE is_checked_out = true
        AND book_id=%s
        )
    ) AS available_copies,
    book_copies.location_id
    FROM library.book_copies
    WHERE library.book_copies.book_id=%s
    AND library.book_copies.is_checked_out = false
    """
    result = exec_get_all(query, (book_id, book_id, book_id, ))
    return result

def is_checked_out(book_copy_id) -> bool:
    query = """
    SELECT book_copies.is_checked_out
    FROM library.book_copies
    WHERE book_copies.book_copy_id=%s
    """
    result = exec_get_all(query, (book_copy_id,))
    return result

"""
Calculates the time the book copy has been checked out given a checked_out_id. 
Returns the number of days the book has been borrowed based on when it was returned
"""
def get_days_borrowed_after_returned(checked_out_id) -> int:
    query = """
    SELECT EXTRACT(day from
        (
        SELECT returned_date
        FROM library.checked_out
        WHERE library.checked_out.checked_out_id=%s
        )::timestamp
        -
        (
        SELECT borrowed_date
        FROM library.checked_out
        WHERE library.checked_out.checked_out_id=%s
        )::timestamp
    ) AS days_borrowed
    """
    result = exec_get_all(query, (checked_out_id, checked_out_id))
    days = int(result[0][0])
    return days
