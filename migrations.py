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

    def upgrade_funcionario_atribuicao(self) -> None:
        self.run_migration('upgrade_funcionario_atribuicao.sql')

    def downgrade_funcionario_atribuicao(self) -> None:
        self.run_migration('downgrade_funcionario_atribuicao.sql')

    def upgrade_funcionario_restricao(self) -> None:
        self.run_migration('upgrade_funcionario_restricao.sql')

    def downgrade_funcionario_restricao(self) -> None:
        self.run_migration('downgrade_funcionario_restricao.sql')

    def upgrade_educador_fisico(self) -> None:
        self.run_migration('upgrade_educador_fisico.sql')

    def downgrade_educador_fisico(self) -> None:
        self.run_migration('downgrade_educador_fisico.sql')

    def upgrade_populated_db(self) -> None:
        print("\tDatabase upgrade (populated)")
        self.upgrade_schema()
        self.upgrade_pessoa()
        self.upgrade_interno_usp()
        self.upgrade_funcionario()
        self.upgrade_funcionario_atribuicao()
        self.upgrade_funcionario_restricao()
        self.upgrade_educador_fisico()

    def downgrade_populated_db(self) -> None:
        """Executa todas as migrações de downgrade com dados populados"""
        print("\tDatabase downgrade (populated)")
        self.downgrade_educador_fisico()
        self.downgrade_funcionario_restricao()
        self.downgrade_funcionario_atribuicao()
        self.downgrade_funcionario()
        self.downgrade_interno_usp()
        self.downgrade_pessoa()
        self.downgrade_schema()