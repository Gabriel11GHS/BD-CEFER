import random
import csv
from pathlib import Path

# Dicionário de instalações
NOMES_INSTALACOES_POR_TIPO = {
    'Quadra': ['Quadra Poliesportiva A', 'Quadra Poliesportiva B', 'Quadra de Tênis 1', 'Quadra de Tênis 2', 'Quadra de Peteca', 'Quadra de Areia Vôlei', 'Quadra de Areia Beach Tennis'],
    'Piscina': ['Piscina Olímpica', 'Piscina Recreativa'],
    'Academia': ['Academia Principal', 'Espaço Multifuncional Musculação'],
    'Sala': ['Sala de Dança', 'Sala de Ginástica', 'Sala de Alongamento', 'Salão de Eventos'],
    'Campo': ['Campo de Futebol Principal', 'Campo de Futebol Society'],
    'Vestiário': ['Vestiário Masculino A', 'Vestiário Feminino A', 'Vestiário Masculino B', 'Vestiário Feminino B']
}

# --- ASSINATURA CORRIGIDA: Aceita DIRETÓRIOS ---
def gerar_instalacoes(sql_dir: Path, csv_dir: Path, num_registros: int):
    """
    Gera dados fictícios para a tabela INSTALACAO e salva em arquivos SQL e CSV.
    Gera um ID sequencial local no CSV para ser usado por outros scripts.
    """
    print(f"Gerando {num_registros} registros para INSTALACAO...")

    # --- NOMES DE ARQUIVO DEFINIDOS INTERNAMENTE ---
    sql_output_path = sql_dir / 'upgrade_instalacao.sql'
    csv_output_path = csv_dir / 'instalacoes.csv'
    # ---------------------------------------------

    instalacoes_data_for_csv = []
    sql_statements = []

    # 1. Preenche a lista de todas as instalações únicas
    instalacoes_unicas = []
    for tipo, nomes in NOMES_INSTALACOES_POR_TIPO.items():
        for nome in nomes:
            instalacoes_unicas.append((nome, tipo))

    # 2. Verifica o limite de registros
    if num_registros > len(instalacoes_unicas):
        print(f"  Aviso: Número de instalações ({num_registros}) maior que o número de nomes únicos disponíveis ({len(instalacoes_unicas)}). Gerando {len(instalacoes_unicas)}.")
        num_registros = len(instalacoes_unicas)

    # 3. Seleciona aleatoriamente
    instalacoes_selecionadas = random.sample(instalacoes_unicas, num_registros)

    # 4. Prepara os dados com ID local
    for id_instalacao_local, (nome, tipo) in enumerate(instalacoes_selecionadas, 1):
        capacidade = random.randint(10, 200)
        eh_reservavel = 'S' if tipo != 'Vestiário' else 'N' # Usar S/N

        # Adiciona o ID ao CSV
        instalacoes_data_for_csv.append([id_instalacao_local, nome, tipo, capacidade, eh_reservavel])

        # SQL não precisa do ID
        nome_sql = nome.replace("'", "''")
        tipo_sql = tipo.replace("'", "''")
        sql = (
            f"INSERT INTO INSTALACAO (NOME, TIPO, CAPACIDADE, EH_RESERVAVEL) "
            f"VALUES ('{nome_sql}', '{tipo_sql}', {capacidade}, '{eh_reservavel}');"
        )
        sql_statements.append(sql)

    # Escreve o arquivo CSV (usando csv_output_path)
    try:
        with open(csv_output_path, 'w', newline='', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)
            # Cabeçalho com ID_INSTALACAO
            writer.writerow(['ID_INSTALACAO', 'NOME', 'TIPO', 'CAPACIDADE', 'EH_RESERVAVEL'])
            writer.writerows(instalacoes_data_for_csv)
        print(f"  Arquivo CSV gerado com sucesso em: {csv_output_path}")
    except Exception as e:
        print(f"  Erro ao gerar arquivo CSV para INSTALACAO: {e}")
        return # Interrompe se não conseguir gerar CSV

    # Escreve o arquivo SQL (usando sql_output_path)
    try:
        with open(sql_output_path, 'w', encoding='utf-8') as file_sql:
            for statement in sql_statements:
                file_sql.write(statement + '\n')
        print(f"  Arquivo SQL gerado com sucesso em: {sql_output_path}")
    except Exception as e:
        print(f"  Erro ao gerar arquivo SQL para INSTALACAO: {e}")