import pytest
from migrations import Migrations

# List all tables that should be created according to the upgrade SQL.
TABLES = [
    "PESSOA",
    "INTERNO_USP",
    "FUNCIONARIO",
    "FUNCIONARIO_ATRIBUICAO",
    "FUNCIONARIO_RESTRICAO",
    "EDUCADOR_FISICO",
    "INSTALACAO",
    "EQUIPAMENTO",
    "DOACAO",
    "RESERVA",
    "ATIVIDADE",
    "OCORRENCIA_SEMANAL",
    "CONDUZ_ATIVIDADE",
    "PARTICIPACAO_ATIVIDADE",
    "EVENTO",
    "SUPERVISAO_EVENTO",
    "GRUPO_EXTENSAO",
    "ATIVIDADE_GRUPO_EXTENSAO",
]

def test_schema_migrations(dbsession):
    migrations = Migrations(schema='tests')
    migrations.upgrade_schema()

    # Tests if tables were created
    with dbsession.connection.cursor() as cursor:
        for table in TABLES:
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'tests' AND lower(table_name) = lower(%s);",
                (table,)
            )
            count = cursor.fetchone()[0]
            assert count == 1, f"Table {table} was not created in schema 'tests'"

    migrations.downgrade_schema()

    # Tests if tables were dropped
    with dbsession.connection.cursor() as cursor:
        for table in TABLES:
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'tests' AND lower(table_name) = lower(%s);",
                (table,)
            )
            count = cursor.fetchone()[0]
            assert count == 0, f"Table {table} still exists in schema 'tests' (count={count})"
