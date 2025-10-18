import pytest
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

def test_upgrade_and_downgrade_populate_db(dbsession):
    migrations = Migrations(dbsession=dbsession)

    migrations.upgrade_populated_db()

    with dbsession.connection.cursor() as cursor:
        assert count_table_records(cursor, 'PESSOA') == 20
        assert count_table_records(cursor, 'INTERNO_USP') == 10
        assert count_table_records(cursor, 'FUNCIONARIO') == 3

    migrations.downgrade_populated_db()

    tables = ["PESSOA", "INTERNO_USP", "FUNCIONARIO", "ATIVIDADE", "INSTALACAO"]
    with dbsession.connection.cursor() as cursor:
        for table in tables:
            assert not table_exists(cursor, table), f"Tabela {table} ainda existe após downgrade"