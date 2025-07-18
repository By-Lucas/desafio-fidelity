import psycopg2
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 5432):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "dbname": database,
            "port": port,
        }

    @contextmanager
    def get_cursor(self):
        conn = psycopg2.connect(**self.config)
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        finally:
            cursor.close()
            conn.close()
