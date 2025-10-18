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
        # Verifica as tabelas de pessoas e internos USP
        assert count_table_records(cursor, 'PESSOA') == 20
        assert count_table_records(cursor, 'INTERNO_USP') == 10
        
        # Verifica as tabelas de funcionários
        assert count_table_records(cursor, 'FUNCIONARIO') == 3
        assert count_table_records(cursor, 'FUNCIONARIO_ATRIBUICAO') == 6
        assert count_table_records(cursor, 'FUNCIONARIO_RESTRICAO') == 1
        assert count_table_records(cursor, 'EDUCADOR_FISICO') == 2
        
        # Verifica as tabelas de instalações e equipamentos
        assert count_table_records(cursor, 'INSTALACAO') == 8
        assert count_table_records(cursor, 'EQUIPAMENTO') == 10
        assert count_table_records(cursor, 'DOACAO') == 3
        
        # Verifica as novas tabelas de atividades e reservas
        assert count_table_records(cursor, 'ATIVIDADE') == 6
        assert count_table_records(cursor, 'OCORRENCIA_SEMANAL') == 15
        assert count_table_records(cursor, 'RESERVA') == 6

    migrations.downgrade_populated_db()

    # Verifica se todas as tabelas foram removidas
    tables = [
        "PESSOA", "INTERNO_USP", "FUNCIONARIO", 
        "FUNCIONARIO_ATRIBUICAO", "FUNCIONARIO_RESTRICAO", "EDUCADOR_FISICO",
        "INSTALACAO", "EQUIPAMENTO", "DOACAO",
        "ATIVIDADE", "OCORRENCIA_SEMANAL", "RESERVA"
    ]
    with dbsession.connection.cursor() as cursor:
        for table in tables:
            assert not table_exists(cursor, table), f"Tabela {table} ainda existe após downgrade"