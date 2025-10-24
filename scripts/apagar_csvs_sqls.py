import os
from pathlib import Path

def apagar_arquivos_gerados():
    """
    Encontra e apaga todos os arquivos .csv e .sql gerados pelo script 
    'gerar_dados.py' nas pastas de destino.
    """
    
    try:
        # Define o caminho raiz do projeto (assumindo que este script está em 'script/')
        PROJECT_ROOT = Path(__file__).parent.parent 
    except NameError:
        # Fallback se executado de forma interativa (não como script)
        PROJECT_ROOT = Path.cwd()

    # Define os diretórios onde os arquivos são gerados
    csv_dir = PROJECT_ROOT / 'sql' / 'csv'
    sql_dir = PROJECT_ROOT / 'sql' / 'populate_mocked_minimal_db'

    # Lista de diretórios para limpar
    diretorios_para_limpar = [csv_dir, sql_dir]
    
    print("Iniciando limpeza dos arquivos gerados...")

    arquivos_apagados = 0
    
    for pasta in diretorios_para_limpar:
        if not pasta.is_dir():
            print(f"Aviso: Diretório não encontrado, pulando: {pasta}")
            continue

        # Encontra todos os arquivos .csv e .sql na pasta
        # Usando .glob() para encontrar os arquivos
        arquivos_csv = list(pasta.glob('*.csv'))
        arquivos_sql = list(pasta.glob('*.sql'))
        
        arquivos_para_apagar = arquivos_csv + arquivos_sql

        if not arquivos_para_apagar:
            print(f"Nenhum arquivo .csv ou .sql encontrado em: {pasta}")
            continue

        for arquivo_path in arquivos_para_apagar:
            try:
                os.remove(arquivo_path)
                print(f"Apagado: {arquivo_path}")
                arquivos_apagados += 1
            except OSError as e:
                print(f"Erro ao apagar {arquivo_path}: {e}")

    if arquivos_apagados > 0:
        print(f"\nLimpeza concluída. Total de {arquivos_apagados} arquivos removidos.")
    else:
        print("\nNenhum arquivo .sql ou .csv foi encontrado nos diretórios de destino.")

if __name__ == "__main__":
    apagar_arquivos_gerados()