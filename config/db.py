import mariadb
from contextlib import contextmanager


class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
        }

    @contextmanager
    def get_cursor(self):
        conn = mariadb.connect(**self.config)
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        finally:
            cursor.close()
            conn.close()
