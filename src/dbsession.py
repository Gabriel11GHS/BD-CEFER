import psycopg2
from psycopg2 import sql

class DBSession:
    def __init__(self, schema: str | None = None):
        self.connection = psycopg2.connect(
            host='localhost',
            port=5432,
            database='public', 
            user='postgres',
            password='password'
        )
        self.schema = schema
        if self.schema:
            try:
                with self.connection.cursor() as cur:
                    cur.execute(sql.SQL("SET search_path TO {};").format(sql.Identifier(self.schema)))
                self.connection.commit()
            except Exception:
                self.connection.rollback()
    
    def run_sql_file(self, path):
        try:
            with open(path, 'r') as file:
                query = file.read()
            with self.connection.cursor() as cursor:
                cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error executing query from file {path}: {e}")

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
