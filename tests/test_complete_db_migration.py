import pytest
from migrations import Migrations

def test_upgrade_db_and_downgrade_db(dbsession):
    migrations = Migrations(dbsession=dbsession) 

    migrations.upgrade_schema() 
    migrations.upgrade_pessoa()

    with dbsession.connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM tests.PESSOA;")
        assert cursor.fetchone()[0] == 20

    migrations.upgrade_interno_usp()
    with dbsession.connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM tests.INTERNO_USP;")
        assert cursor.fetchone()[0] == 10

    migrations.downgrade_interno_usp()

    with dbsession.connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM tests.INTERNO_USP;")
        assert cursor.fetchone()[0] == 0
