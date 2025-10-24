from src.dbsession import DBSession
from src.migrations import PopulateMockedMinimalDbMigration

def downgrade_db():
    # Criando a sessão do banco
    dbsession = DBSession()  
    
    # Criando a instância da migração
    migration = PopulateMockedMinimalDbMigration(dbsession=dbsession)
    
    # Executando a migração de downgrade
    print("Iniciando o downgrade do banco...")
    migration.downgrade_populated_db()  # Chama o método que faz o downgrade
    print("Downgrade concluído com sucesso!")

if __name__ == "__main__":
    downgrade_db()
