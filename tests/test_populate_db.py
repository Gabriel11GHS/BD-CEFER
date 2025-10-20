import pytest
from collections import OrderedDict

from migrations import Migrations

def count_table_records(cursor, table_name, schema='tests'):
    """Função auxiliar para contar registros em uma tabela"""
    cursor.execute(f"SELECT COUNT(*) FROM {schema}.{table_name};")
    return cursor.fetchone()[0]

def table_exists(cursor, table_name, schema='tests'):
    """Função auxiliar para verificar se uma tabela existe"""
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = %s AND table_name = lower(%s);
        """,
        (schema, table_name)
    )
    return cursor.fetchone()[0] > 0

def verify_expected_tables_records(cursor, EXPECTED_TABLES_RECORDS):
    """Verifica se as tabelas têm a quantidade esperada de registros"""
    for table_name, expected_count in EXPECTED_TABLES_RECORDS.items():
        actual_count = count_table_records(cursor, table_name)
        assert actual_count == expected_count, (
            f"Tabela {table_name}: esperado {expected_count}, "
            f"obtido {actual_count}"
        )

def verify_tables_removed(cursor, tables):
    """Verifica se todas as tabelas foram removidas após downgrade"""
    for table_name in tables:
        assert not table_exists(cursor, table_name), (
            f"Tabela {table_name} ainda existe após downgrade"
        )

def test_upgrade_and_downgrade_populate_db(dbsession):
    EXPECTED_TABLES_RECORDS = OrderedDict([
        ('PESSOA', 20),
        ('INTERNO_USP', 10),
        ('FUNCIONARIO', 3),
        ('FUNCIONARIO_ATRIBUICAO', 6),
        ('FUNCIONARIO_RESTRICAO', 1),
        ('EDUCADOR_FISICO', 2),
        ('INSTALACAO', 8),
        ('EQUIPAMENTO', 10),
        ('DOACAO', 3),
        ('ATIVIDADE', 6),
        ('OCORRENCIA_SEMANAL', 15),
        ('RESERVA', 6),
        ('CONDUZ_ATIVIDADE', 6),
        ('PARTICIPACAO_ATIVIDADE', 10),
        ('EVENTO', 4),
        ('SUPERVISAO_EVENTO', 5),
        ('GRUPO_EXTENSAO', 4),
        ('ATIVIDADE_GRUPO_EXTENSAO', 6)
    ])

    ALL_TABLES = list(EXPECTED_TABLES_RECORDS.keys())

    migrations = Migrations(dbsession=dbsession)
    migrations.upgrade_populated_db()

    with dbsession.connection.cursor() as cursor:
        verify_expected_tables_records(cursor, EXPECTED_TABLES_RECORDS)

    migrations.downgrade_populated_db()

    with dbsession.connection.cursor() as cursor:
        verify_tables_removed(cursor, ALL_TABLES)