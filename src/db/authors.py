from .swen344_db_utils import exec_get_all
from .library_schema import authenticate_user
import json

def get_all(session_key) -> json:
    data = []
    if authenticate_user(session_key):
        query = """
            SELECT authors.author_id,
                STRING_AGG (
                    authors.first_name || ' ' || authors.last_name, ','
                    ORDER BY authors.first_name, authors.last_name
                ) author_list
            FROM library.authors
            GROUP BY authors.author_id
            """
        result = exec_get_all(query, )
        columns = ["author id", "full name"]
        
        for book in result:
            location = []
            for i in range(len(columns)):
                location.append((columns[i], book[i]))
            data.append(dict(location))

    jdata = json.dumps(data)
    return jdata

def wrote(session_key, author_id) -> json:
    data = []
    if authenticate_user(session_key):
        query = """
            SELECT books.title
            FROM library.books
            INNER JOIN library.wrote USING (book_id)
            INNER JOIN library.authors USING (author_id)
            WHERE authors.author_id=%s
            """
        result = exec_get_all(query, (author_id, ))
        columns = ["title"]
        for book in result:
            location = []
            for i in range(len(columns)):
                location.append((columns[i], book[i]))
            data.append(dict(location))

    jdata = json.dumps(data)
    return jdata
