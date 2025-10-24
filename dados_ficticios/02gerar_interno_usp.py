import csv
import random

# Função para gerar um NUSP aleatório (exemplo)
def gerar_nusp():
    return f"{random.randint(1000000000, 9999999999)}"

# Função para gerar uma categoria aleatória
def gerar_categoria():
    categorias = ['ALUNO_GRADUACAO', 'ALUNO_MESTRADO', 'ALUNO_DOUTORADO', 'FUNCIONARIO']
    return random.choice(categorias)

# Função para dividir os dados em 90% para o arquivo SQL e 10% para o arquivo CSV
def gerar_interno_usp(nome_arquivo_entrada, nome_arquivo_sql, nome_arquivo_csv_90, nome_arquivo_csv_10):
    with open(nome_arquivo_entrada, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Ignora o cabeçalho
        pessoas = list(reader)

    # Embaralhar os dados para garantir a aleatoriedade
    random.shuffle(pessoas)

    # Calcular a quantidade para 90% e 10%
    total_pessoas = len(pessoas)
    percentual_90 = int(total_pessoas * 0.9)
    
    # Separar os dados
    pessoas_90 = pessoas[:percentual_90]
    pessoas_10 = pessoas[percentual_90:]

    # Função para salvar os dados no arquivo SQL
    def salvar_no_sql(pessoas_90):
        with open(nome_arquivo_sql, mode='w', encoding='utf-8') as sql_file:
            for row in pessoas_90:
                cpf_pessoa = row[0]
                nusp = gerar_nusp()
                categoria = gerar_categoria()

                # Gerar o comando SQL de inserção
                insert_sql = f"INSERT INTO INTERNO_USP (CPF_PESSOA, NUSP, CATEGORIA) VALUES ('{cpf_pessoa}', '{nusp}', '{categoria}');\n"
                sql_file.write(insert_sql)  # Escrever o comando no arquivo .sql

    # Função para salvar os dados no arquivo CSV
    def salvar_no_csv(pessoas, nome_arquivo_csv):
        with open(nome_arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Escrever o cabeçalho
            writer.writerows(pessoas)  # Escrever os dados no arquivo CSV

    # Salvar os dados nos respectivos arquivos
    salvar_no_sql(pessoas_90)
    salvar_no_csv(pessoas_90, nome_arquivo_csv_90)
    salvar_no_csv(pessoas_10, nome_arquivo_csv_10)

    print(f"Arquivo SQL gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV dos 90% gerado: {nome_arquivo_csv_90}")
    print(f"Arquivo CSV dos 10% gerado: {nome_arquivo_csv_10}")

# Gerar os arquivos para os dados
dividir_dados('pessoas.csv', 'upgrade_interno_usp.sql', 'pessoas_internas.csv', 'pessoas_restantes.csv')
