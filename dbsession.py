import psycopg2
from psycopg2 import sql

class DBSession:
    def __init__(self, schema: str | None = None):
        """Open a DB connection. If `schema` is provided, set the session
        search_path to that schema so subsequent SQL runs operate there.
        """
        self.connection = psycopg2.connect(
            host='localhost',
            port=5432,
            database='public', 
            user='postgres',
            password='password'
        )
        self.schema = schema
        if self.schema:
            # set the search_path safely using an identifier
            try:
                with self.connection.cursor() as cur:
                    cur.execute(sql.SQL("SET search_path TO {};").format(sql.Identifier(self.schema)))
                self.connection.commit()
            except Exception:
                # If setting search_path fails, rollback and continue (errors will surface on use)
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