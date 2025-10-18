import pytest
from migrations import Migrations

def test_upgrade_and_downgrade_populate_db(dbsession):
    migrations = Migrations(dbsession=dbsession)

    migrations.upgrade_populated_db()

    with dbsession.connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM tests.PESSOA;")
        assert cursor.fetchone()[0] == 20

        cursor.execute("SELECT COUNT(*) FROM tests.INTERNO_USP;")
        assert cursor.fetchone()[0] == 10

    migrations.downgrade_populated_db()

    tables = ["PESSOA", "INTERNO_USP", "FUNCIONARIO", "ATIVIDADE", "INSTALACAO"]
    with dbsession.connection.cursor() as cursor:
        for table in tables:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'tests' AND table_name = lower(%s);
                """,
                (table,)
            )
            count = cursor.fetchone()[0]
            assert count == 0, f"Tabela {table} ainda existe após downgrade"
