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

    def upgrade_funcionario_atribuicao(self):
        self.run_migration('upgrade_funcionario_atribuicao.sql')

    def downgrade_funcionario_atribuicao(self):
        self.run_migration('downgrade_funcionario_atribuicao.sql')

    def upgrade_funcionario_restricao(self):
        self.run_migration('upgrade_funcionario_restricao.sql')

    def downgrade_funcionario_restricao(self):
        self.run_migration('downgrade_funcionario_restricao.sql')

    def upgrade_educador_fisico(self):
        self.run_migration('upgrade_educador_fisico.sql')

    def downgrade_educador_fisico(self):
        self.run_migration('downgrade_educador_fisico.sql')

    def upgrade_instalacao(self):
        self.run_migration('upgrade_instalacao.sql')

    def downgrade_instalacao(self):
        self.run_migration('downgrade_instalacao.sql')

    def upgrade_equipamento(self):
        self.run_migration('upgrade_equipamento.sql')

    def downgrade_equipamento(self):
        self.run_migration('downgrade_equipamento.sql')

    def upgrade_doacao(self):
        self.run_migration('upgrade_doacao.sql')

    def downgrade_doacao(self):
        self.run_migration('downgrade_doacao.sql')

    def upgrade_atividade(self):
        self.run_migration('upgrade_atividade.sql')

    def downgrade_atividade(self):
        self.run_migration('downgrade_atividade.sql')

    def upgrade_ocorrencia_semanal(self):
        self.run_migration('upgrade_ocorrencia_semanal.sql')

    def downgrade_ocorrencia_semanal(self):
        self.run_migration('downgrade_ocorrencia_semanal.sql')

    def upgrade_reserva(self):
        self.run_migration('upgrade_reserva.sql')

    def downgrade_reserva(self):
        self.run_migration('downgrade_reserva.sql')

    def upgrade_conduz_atividade(self) -> None:
        self.run_migration('upgrade_conduz_atividade.sql')

    def downgrade_conduz_atividade(self) -> None:
        self.run_migration('downgrade_conduz_atividade.sql')

    def upgrade_participacao_atividade(self) -> None:
        self.run_migration('upgrade_participacao_atividade.sql')

    def downgrade_participacao_atividade(self) -> None:
        self.run_migration('downgrade_participacao_atividade.sql')

    def upgrade_evento(self) -> None:
        self.run_migration('upgrade_evento.sql')

    def downgrade_evento(self) -> None:
        self.run_migration('downgrade_evento.sql')

    def upgrade_supervisao_evento(self) -> None:
        self.run_migration('upgrade_supervisao_evento.sql')

    def downgrade_supervisao_evento(self) -> None:
        self.run_migration('downgrade_supervisao_evento.sql')

    def upgrade_populated_db(self) -> None:
        self.upgrade_schema()
        self.upgrade_pessoa()
        self.upgrade_interno_usp()
        self.upgrade_funcionario()
        self.upgrade_funcionario_atribuicao()
        self.upgrade_funcionario_restricao()
        self.upgrade_educador_fisico()
        self.upgrade_instalacao()
        self.upgrade_equipamento()
        self.upgrade_doacao()
        self.upgrade_atividade()
        self.upgrade_ocorrencia_semanal()
        self.upgrade_reserva()
        self.upgrade_conduz_atividade()
        self.upgrade_participacao_atividade()
        self.upgrade_evento()
        self.upgrade_supervisao_evento()

    def downgrade_populated_db(self) -> None:
        self.downgrade_supervisao_evento()
        self.downgrade_evento()
        self.downgrade_participacao_atividade()
        self.downgrade_conduz_atividade()
        self.downgrade_reserva()
        self.downgrade_ocorrencia_semanal()
        self.downgrade_atividade()
        self.downgrade_doacao()
        self.downgrade_equipamento()
        self.downgrade_instalacao()
        self.downgrade_educador_fisico()
        self.downgrade_funcionario_restricao()
        self.downgrade_funcionario_atribuicao()
        self.downgrade_funcionario()
        self.downgrade_interno_usp()
        self.downgrade_pessoa()
        self.downgrade_schema()