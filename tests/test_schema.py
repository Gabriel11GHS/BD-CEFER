# test_schema.py
import pytest
from migrations import Migrations

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
    migrations = Migrations(dbsession=dbsession)
    
    migrations.upgrade('schema')

    with dbsession.connection.cursor() as cursor:
        for table in TABLES:
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'tests' AND lower(table_name) = lower(%s);",
                (table,)
            )
            count = cursor.fetchone()[0]
            assert count == 1, f"Table {table} was not created in schema 'tests'"

    migrations.downgrade('schema')

    with dbsession.connection.cursor() as cursor:
        for table in TABLES:
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'tests' AND lower(table_name) = lower(%s);",
                (table,)
            )
            count = cursor.fetchone()[0]
            assert count == 0, f"Table {table} still exists in schema 'tests'"