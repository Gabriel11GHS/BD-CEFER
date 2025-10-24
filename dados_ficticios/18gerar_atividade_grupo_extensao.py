import csv
import random

def gerar_atividade_grupo_extensao(
    nome_arquivo_atividades,
    nome_arquivo_grupos,
    nome_arquivo_sql,
    nome_arquivo_csv
):
    # Ler atividades
    with open(nome_arquivo_atividades, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Pula cabeçalho
        atividades = list(reader)

    # Ler grupos de extensão
    with open(nome_arquivo_grupos, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        grupos = list(reader)

    # Obter listas simplificadas
    id_atividades = [i + 1 for i in range(len(atividades))]  # IDs sequenciais (se ID_ATIVIDADE for identity)
    nomes_grupos = [g[0] for g in grupos]

    registros = []

    # Para cada grupo, associar de 1 a 5 atividades aleatórias
    for grupo in nomes_grupos:
        num_atividades = random.randint(1, 5)
        atividades_escolhidas = random.sample(id_atividades, num_atividades)
        for id_atividade in atividades_escolhidas:
            registros.append([id_atividade, grupo])

    # Criar arquivo SQL
    with open(nome_arquivo_sql, mode='w', encoding='utf-8') as sql_file:
        for reg in registros:
            id_atividade = reg[0]
            nome_grupo = reg[1].replace("'", "''")
            insert_sql = (
                f"INSERT INTO ATIVIDADE_GRUPO_EXTENSAO (ID_ATIVIDADE, NOME_GRUPO) "
                f"VALUES ({id_atividade}, '{nome_grupo}');\n"
            )
            sql_file.write(insert_sql)

    # Criar arquivo CSV
    with open(nome_arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_ATIVIDADE', 'NOME_GRUPO'])
        writer.writerows(registros)

    print(f"Arquivo SQL gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV gerado: {nome_arquivo_csv}")
    print(f"Total de vínculos gerados: {len(registros)}")

# Exemplo de uso
if __name__ == "__main__":
    gerar_atividade_grupo_extensao(
        nome_arquivo_atividades='atividades.csv',
        nome_arquivo_grupos='grupos_extensao.csv',
        nome_arquivo_sql='upgrade_atividade_grupo_extensao.sql',
        nome_arquivo_csv='atividade_grupo_extensao.csv'
    )
