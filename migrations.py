from dbsession import DBSession

class Migrations:
    def __init__(self, dbsession: DBSession):
        """Usa a DBSession existente"""
        self.dbsession = dbsession
        self.folder = './sql'

    def run_migration(self, file: str, action: str) -> None:
        path = f'{self.folder}/{file}'
        self.dbsession.run_sql_file(path)

    def upgrade_schema(self) -> None:
        self.run_migration('upgrade_schema.sql', 'Creating schema')

    def downgrade_schema(self) -> None:
        self.run_migration('downgrade_schema.sql', 'Dropping schema')

    def upgrade_pessoa(self) -> None:
        self.run_migration('upgrade_pessoa.sql', 'Adding pessoas')

    def downgrade_pessoa(self) -> None:
        self.run_migration('downgrade_pessoa.sql', 'Removing pessoas')

    def upgrade_interno_usp(self) -> None:
        self.run_migration('upgrade_interno_usp.sql', 'Adding internos')

    def downgrade_interno_usp(self) -> None:
        self.run_migration('downgrade_interno_usp.sql', 'Removing internos')
