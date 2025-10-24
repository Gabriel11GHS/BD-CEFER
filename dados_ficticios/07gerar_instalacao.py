import random
import csv
from pathlib import Path # Importar Path para lidar com caminhos

# Supondo que NOMES_INSTALACOES_POR_TIPO seja um dicionário definido em algum lugar
# Exemplo:
NOMES_INSTALACOES_POR_TIPO = {
    'Quadra': ['Quadra Poliesportiva A', 'Quadra Poliesportiva B', 'Quadra de Tênis 1', 'Quadra de Tênis 2', 'Quadra de Peteca', 'Quadra de Areia Vôlei', 'Quadra de Areia Beach Tennis'],
    'Piscina': ['Piscina Olímpica', 'Piscina Recreativa'],
    'Academia': ['Academia Principal', 'Espaço Multifuncional Musculação'],
    'Sala': ['Sala de Dança', 'Sala de Ginástica', 'Sala de Alongamento', 'Salão de Eventos'],
    'Campo': ['Campo de Futebol Principal', 'Campo de Futebol Society'],
    'Vestiário': ['Vestiário Masculino A', 'Vestiário Feminino A', 'Vestiário Masculino B', 'Vestiário Feminino B']
}

def gerar_instalacoes(sql_output_path: Path, csv_output_path: Path, num_registros: int):
    """
    Gera dados fictícios para a tabela INSTALACAO e salva em arquivos SQL e CSV.

    Args:
        sql_output_path: Caminho completo (objeto Path) para o arquivo .sql de saída.
        csv_output_path: Caminho completo (objeto Path) para o arquivo .csv de saída.
        num_registros: Quantidade de instalações a serem geradas.
    """
    print(f"Gerando {num_registros} registros para INSTALACAO...")
    instalacoes_data_for_csv = [] # Lista para dados do CSV
    sql_statements = [] # Lista para comandos SQL

    instalacoes_unicas = []
    for tipo, nomes in NOMES_INSTALACOES_POR_TIPO.items():
        for nome in nomes:
            instalacoes_unicas.append((nome, tipo))

    if num_registros > len(instalacoes_unicas):
        print(f"  Aviso: Número de instalações ({num_registros}) é maior que o número de nomes únicos disponíveis ({len(instalacoes_unicas)}). Gerando {len(instalacoes_unicas)}.")
        num_registros = len(instalacoes_unicas)

    instalacoes_selecionadas = random.sample(instalacoes_unicas, num_registros)

    # Prepara os dados e comandos SQL
    for nome, tipo in instalacoes_selecionadas:
        capacidade = random.randint(10, 200)
        eh_reservavel = 'Sim' if tipo != 'Vestiário' else 'Nao'
        
        # Dados para CSV (sem ID, pois será gerado pelo BD)
        instalacoes_data_for_csv.append([nome, tipo, capacidade, eh_reservavel])

        nome_sql = nome.replace("'", "''")
        tipo_sql = tipo.replace("'", "''")
        sql = (
            f"INSERT INTO INSTALACAO (NOME, TIPO, CAPACIDADE, EH_RESERVAVEL) "
            f"VALUES ('{nome_sql}', '{tipo_sql}', {capacidade}, '{eh_reservavel}');"
        )
        sql_statements.append(sql)

    # Escreve o arquivo CSV
    try:
        with open(csv_output_path, 'w', newline='', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)
            # Cabeçalho adaptado para refletir o que está sendo salvo (sem ID)
            writer.writerow(['NOME', 'TIPO', 'CAPACIDADE', 'EH_RESERVAVEL'])
            writer.writerows(instalacoes_data_for_csv)
        print(f"  Arquivo CSV gerado com sucesso em: {csv_output_path}")
    except Exception as e:
        print(f"  Erro ao gerar arquivo CSV para INSTALACAO: {e}")
        return # Interrompe se não conseguir gerar CSV

    # Escreve o arquivo SQL
    try:
        with open(sql_output_path, 'w', encoding='utf-8') as file_sql:
            for statement in sql_statements:
                file_sql.write(statement + '\n')
        print(f"  Arquivo SQL gerado com sucesso em: {sql_output_path}")
    except Exception as e:
        print(f"  Erro ao gerar arquivo SQL para INSTALACAO: {e}")
