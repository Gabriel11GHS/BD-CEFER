import random
import csv
from pathlib import Path

NOMES_GRUPOS_EXTENSAO = [
    'Grupo de Karatê Shotokan', 
    'Equipe Kung Fu Garra de Águia', 
    'Grupo de Estudos Tai Chi Chuan', 
    'Projeto Capoeira Angola'
]

def gerar_grupo_extensao(
    sql_dir: Path, 
    csv_dir: Path, 
    num_registros: int, 
    internos_csv_path: Path
):
    """
    Gera dados fictícios para GRUPO_EXTENSAO e salva nos diretórios 
    especificados, lendo CPFs de internos do CSV.
    """
    print(f"Gerando dados para GRUPO_EXTENSAO...")

    # --- 1. Definir caminhos de saída ---
    sql_output_path = sql_dir / 'upgrade_grupo_extensao.sql'
    csv_output_path = csv_dir / 'grupos_extensao.csv'

    # --- 2. Ler CPFs de internos do CSV ---
    cpfs_internos = []
    try:
        with open(internos_csv_path, 'r', encoding='utf-8') as f_internos:
            reader = csv.reader(f_internos)
            header = next(reader) # Pular cabeçalho
            try:
                # Assumindo que o CSV de internos tenha uma coluna 'CPF'
                idx_cpf = header.index('CPF') 
            except ValueError:
                print(f"  Erro: Cabeçalho 'CPF' não encontrado em {internos_csv_path}")
                return
            
            for row in reader:
                cpfs_internos.append(row[idx_cpf])
                
        if not cpfs_internos:
            print("  Aviso: Nenhum CPF de interno encontrado no arquivo CSV.")
            return
            
    except FileNotFoundError:
        print(f"  Erro: Arquivo de internos não encontrado em {internos_csv_path}")
        return
    except Exception as e:
        print(f"  Erro ao ler arquivo de internos: {e}")
        return

    # --- 3. Lógica de Geração (adaptada do original) ---
    grupos_data_for_csv = []
    sql_statements = []

    num_a_selecionar = min(num_registros, len(NOMES_GRUPOS_EXTENSAO))
    if num_registros > len(NOMES_GRUPOS_EXTENSAO):
        print(f"  Aviso: Número de registros ({num_registros}) maior que os nomes disponíveis ({len(NOMES_GRUPOS_EXTENSAO)}). Gerando {num_a_selecionar}.")
        
    nomes_selecionados = random.sample(NOMES_GRUPOS_EXTENSAO, num_a_selecionar)

    for nome in nomes_selecionados:
        descricao = f"Grupo de extensão: {nome} promovido pelo CEFER."
        cpf_responsavel = random.choice(cpfs_internos)
        
        # Dados para CSV (NOME_GRUPO é a PK, não há ID serial)
        grupos_data_for_csv.append([nome, descricao, cpf_responsavel])

        # Comando SQL
        # Escapa aspas simples no nome e descrição
        nome_sql = nome.replace("'", "''")
        descricao_sql = descricao.replace("'", "''")
        
        sql = (
            f"INSERT INTO GRUPO_EXTENSAO (NOME_GRUPO, DESCRICAO, CPF_RESPONSAVEL_INTERNO) "
            f"VALUES ('{nome_sql}', '{descricao_sql}', '{cpf_responsavel}');"
        )
        sql_statements.append(sql)

    # --- 4. Escrever arquivos ---
    # Escreve CSV
    try:
        with open(csv_output_path, 'w', newline='', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)
            # Cabeçalho
            writer.writerow(['NOME_GRUPO', 'DESCRICAO', 'CPF_RESPONSAVEL_INTERNO'])
            writer.writerows(grupos_data_for_csv)
        print(f"  Arquivo CSV gerado com sucesso em: {csv_output_path}")
    except Exception as e:
        print(f"  Erro ao gerar arquivo CSV para GRUPO_EXTENSAO: {e}")
        return

    # Escreve SQL
    try:
        with open(sql_output_path, 'w', encoding='utf-8') as file_sql:
            for statement in sql_statements:
                file_sql.write(statement + '\n')
        print(f"  Arquivo SQL gerado com sucesso em: {sql_output_path}")
        print(f"  Inseridos {len(grupos_data_for_csv)} registros em GRUPO_EXTENSAO.")
    except Exception as e:
        print(f"  Erro ao gerar arquivo SQL para GRUPO_EXTENSAO: {e}")