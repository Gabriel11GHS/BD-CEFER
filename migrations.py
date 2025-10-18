from dbsession import DBSession
from pathlib import Path

class Migrations:
    def __init__(self, dbsession: DBSession):
        """Usa a DBSession existente"""
        self.dbsession = dbsession
        self.folder = Path('./sql')

    def run_migration(self, file: str):
        path = self.folder / file
        self.dbsession.run_sql_file(path)

    def upgrade_schema(self):
        self.run_migration('upgrade_schema.sql')

    def downgrade_schema(self):
        self.run_migration('downgrade_schema.sql')

    def upgrade_pessoa(self):
        self.run_migration('upgrade_pessoa.sql')

    def downgrade_pessoa(self):
        self.run_migration('downgrade_pessoa.sql')

    def upgrade_interno_usp(self):
        self.run_migration('upgrade_interno_usp.sql')

    def downgrade_interno_usp(self):
        self.run_migration('downgrade_interno_usp.sql')

    def upgrade_funcionario(self):
        self.run_migration('upgrade_funcionario.sql')

    def downgrade_funcionario(self):
        self.run_migration('downgrade_funcionario.sql')

    def upgrade_populated_db(self) -> None:
        self.upgrade_schema()
        self.upgrade_pessoa()
        self.upgrade_interno_usp()
        self.upgrade_funcionario()

    def downgrade_populated_db(self) -> None:
            self.downgrade_funcionario()
            self.downgrade_interno_usp()
            self.downgrade_pessoa()
            self.downgrade_schema()