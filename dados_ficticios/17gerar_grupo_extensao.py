import csv
import random
from faker import Faker

fake = Faker('pt_BR')

def gerar_grupos_extensao(
    nome_arquivo_internos,
    nome_arquivo_sql,
    nome_arquivo_csv,
    quantidade_grupos=50
):
    # Ler CPFs dos internos
    with open(nome_arquivo_internos, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Ignora cabeçalho
        pessoas_internas = [row[0] for row in reader]  # Coluna CPF

    grupos = []

    # Gerar grupos de extensão
    for _ in range(quantidade_grupos):
        nome_grupo = f"Grupo de Extensão {fake.word().capitalize()} {random.randint(1, 99)}"
        descricao = fake.paragraph(nb_sentences=random.randint(2, 5))
        cpf_responsavel = random.choice(pessoas_internas)

        grupos.append([nome_grupo, descricao, cpf_responsavel])

    # Criar arquivo SQL
    with open(nome_arquivo_sql, mode='w', encoding='utf-8') as sql_file:
        for grupo in grupos:
            nome = grupo[0].replace("'", "''")
            descricao = grupo[1].replace("'", "''")
            cpf = grupo[2]
            insert_sql = (
                f"INSERT INTO GRUPO_EXTENSAO (NOME_GRUPO, DESCRICAO, CPF_RESPONSAVEL_INTERNO) "
                f"VALUES ('{nome}', '{descricao}', '{cpf}');\n"
            )
            sql_file.write(insert_sql)

    # Criar arquivo CSV
    with open(nome_arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['NOME_GRUPO', 'DESCRICAO', 'CPF_RESPONSAVEL_INTERNO'])
        writer.writerows(grupos)

    print(f"Arquivo SQL de grupos gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV de grupos gerado: {nome_arquivo_csv}")
    print(f"Total de grupos gerados: {len(grupos)}")

# Exemplo de uso
if __name__ == "__main__":
    gerar_grupos_extensao(
        nome_arquivo_internos='pessoas_internas.csv',
        nome_arquivo_sql='upgrade_grupo_extensao.sql',
        nome_arquivo_csv='grupos_extensao.csv',
        quantidade_grupos=50  # Pode ajustar conforme quiser
    )
