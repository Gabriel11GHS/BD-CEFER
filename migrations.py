from dbsession import DBSession
from datetime import datetime


class Migrations:
    def __init__(self, dbsession=DBSession, schema: str | None = None):
        """Simple migrations helper.

        If `schema` is provided (a string), internally create a small factory
        that returns DBSession(schema=schema) so callers can simply pass
        `schema='tests'`.
        """
        if schema is not None:
            def factory():
                return DBSession(schema=schema)

            self.dbsession = factory
        else:
            self.dbsession = dbsession

        self.folder = './sql'

    def run_migration(self, file: str) -> None:
        path = f'{self.folder}/{file}'
        print(f"[{datetime.now().isoformat()}] migrations: starting migration {path}")
        with self.dbsession() as db:
            db.run_sql_file(path)
        print(f"[{datetime.now().isoformat()}] migrations: finished migration {path}")

    def upgrade_schema(self) -> None:
        self.run_migration('upgrade_schema.sql')

    def downgrade_schema(self) -> None:
        self.run_migration('downgrade_schema.sql')

