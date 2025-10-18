# migrations.py
from dbsession import DBSession
from pathlib import Path

class Migrations:
    def __init__(self, dbsession: DBSession):
        self.dbsession = dbsession
        self.folder = Path('./sql')
        
        self.migration_order = [
            'schema',
            'pessoa', 
            'interno_usp',
            'funcionario',
            'funcionario_atribuicao',
            'funcionario_restricao',
            'educador_fisico',
            'instalacao',
            'equipamento',
            'doacao',
            'atividade',
            'ocorrencia_semanal', 
            'reserva',
            'conduz_atividade',
            'participacao_atividade',
            'evento',
            'supervisao_evento',
            'grupo_extensao',
            'atividade_grupo_extensao'
        ]

    def run_migration(self, file: str):
        path = self.folder / file
        self.dbsession.run_sql_file(path)

    def upgrade(self, migration_name: str):
        """Executa upgrade de uma migração específica"""
        self.run_migration(f'upgrade_{migration_name}.sql')

    def downgrade(self, migration_name: str):
        """Executa downgrade de uma migração específica"""
        self.run_migration(f'downgrade_{migration_name}.sql')

    def upgrade_populated_db(self):
        """Executa todos os upgrades na ordem correta"""
        for migration_name in self.migration_order:
            self.upgrade(migration_name)

    def downgrade_populated_db(self):
        """Executa todos os downgrades na ordem reversa"""
        for migration_name in reversed(self.migration_order):
            self.downgrade(migration_name)