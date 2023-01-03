from .swen344_db_utils import exec_get_all, exec_sql_file

def rebuild_tables() -> None:
    sql_path = 'src/db/library.sql'
    exec_sql_file(sql_path)

def populate_tables(data_path) -> None:
    exec_sql_file(data_path)

def authenticate_user(session_key) -> bool:
    query = """
        SELECT users.session_key
        FROM library.users
        WHERE users.session_key=%s;
        """
    result = exec_get_all(query, (session_key, ))
    return result[0] != []