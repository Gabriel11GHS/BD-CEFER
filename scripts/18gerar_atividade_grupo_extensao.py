import random
import csv
from pathlib import Path

def gerar_atividade_grupo_extensao(
    sql_dir: Path, 
    csv_dir: Path, 
    atividades_csv_path: Path,
    grupos_extensao_csv_path: Path
):
    """
    Associa atividades a grupos de extensão (lendo de CSVs) 
    e salva nos diretórios especificados.
    """
    print("Gerando dados para ATIVIDADE_GRUPO_EXTENSAO...")

    # --- 1. Definir caminhos de saída ---
    sql_output_path = sql_dir / 'upgrade_atividade_grupo_extensao.sql'
    csv_output_path = csv_dir / 'atividade_grupo_extensao.csv'

    # --- 2. Ler IDs de Atividades do CSV ---
    ids_atividades = []
    try:
        with open(atividades_csv_path, 'r', encoding='utf-8') as f_ativ:
            reader = csv.reader(f_ativ)
            header = next(reader) # Pular cabeçalho
            try:
                # Tenta encontrar 'ID_ATIVIDADE', senão assume a primeira coluna
                idx_id_ativ = header.index('ID_ATIVIDADE')
            except ValueError:
                print(f"  Aviso: Cabeçalho 'ID_ATIVIDADE' não encontrado em {atividades_csv_path}. Assumindo ID sequencial.")
                idx_id_ativ = -1 # Flag para usar ID sequencial

            for i, row in enumerate(reader):
                if idx_id_ativ != -1:
                    try:
                        # Pega o ID da coluna correta
                        id_str = row[idx_id_ativ] if row[idx_id_ativ] else None
                        ids_atividades.append(int(id_str if id_str else i + 1))
                    except (IndexError, ValueError):
                        ids_atividades.append(i + 1) # Fallback se a linha for curta ou o valor inválido
                else:
                    ids_atividades.append(i + 1) # Fallback para ID sequencial

        if not ids_atividades:
            print("  Aviso: Nenhuma atividade encontrada no arquivo CSV.")
            return
            
    except FileNotFoundError:
        print(f"  Erro: Arquivo de atividades não encontrado em {atividades_csv_path}")
        return
    except Exception as e:
        print(f"  Erro ao ler {atividades_csv_path}: {e}")
        return

    # --- 3. Ler Nomes de Grupos do CSV ---
    nomes_grupos = []
    try:
        with open(grupos_extensao_csv_path, 'r', encoding='utf-8') as f_grupos:
            reader = csv.reader(f_grupos)
            header = next(reader) # Pular cabeçalho
            try:
                idx_nome_grupo = header.index('NOME_GRUPO')
            except ValueError:
                print(f"  Erro: Cabeçalho 'NOME_GRUPO' não encontrado em {grupos_extensao_csv_path}")
                return
            
            for row in reader:
                nomes_grupos.append(row[idx_nome_grupo])
                
        if not nomes_grupos:
            print("  Aviso: Nenhum nome de grupo encontrado no arquivo CSV.")
            return
            
    except FileNotFoundError:
        print(f"  Erro: Arquivo de grupos não encontrado em {grupos_extensao_csv_path}")
        return
    except Exception as e:
        print(f"  Erro ao ler {grupos_extensao_csv_path}: {e}")
        return

    # --- 4. Lógica de Geração (adaptada do original) ---
    atividade_grupo_data_for_csv = []
    sql_statements = []

    for id_atividade in ids_atividades:
        nome_grupo = random.choice(nomes_grupos)
        
        # Dados para CSV
        atividade_grupo_data_for_csv.append([id_atividade, nome_grupo])

        # Comando SQL
        # Escapa aspas simples no nome do grupo
        nome_grupo_sql = nome_grupo.replace("'", "''")
        
        sql = (
            f"INSERT INTO ATIVIDADE_GRUPO_EXTENSAO (ID_ATIVIDADE, NOME_GRUPO) "
            f"VALUES ({id_atividade}, '{nome_grupo_sql}');"
        )
        sql_statements.append(sql)
        
    # Escreve CSV
    try:
        with open(csv_output_path, 'w', newline='', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerow(['ID_ATIVIDADE', 'NOME_GRUPO']) # Cabeçalho
            writer.writerows(atividade_grupo_data_for_csv)
        print(f"  Arquivo CSV gerado com sucesso em: {csv_output_path}")
    except Exception as e:
        print(f"  Erro ao gerar arquivo CSV para ATIVIDADE_GRUPO_EXTENSAO: {e}")
        return

    # Escreve SQL
    try:
        with open(sql_output_path, 'w', encoding='utf-8') as file_sql:
            for statement in sql_statements:
                file_sql.write(statement + '\n')
        print(f"  Arquivo SQL gerado com sucesso em: {sql_output_path}")
        print(f"  Inseridos {len(atividade_grupo_data_for_csv)} registros em ATIVIDADE_GRUPO_EXTENSAO.")
    except Exception as e:
        print(f"  Erro ao gerar arquivo SQL para ATIVIDADE_GRUPO_EXTENSAO: {e}")
