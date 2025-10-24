import csv
import random

# Função para gerar uma formação aleatória (exemplo)
def gerar_formacao():
    formacoes = ['Bacharelado', 'Mestrado', 'Doutorado', 'Técnico', 'Especialização']
    return random.choice(formacoes)

# Função para gerar funcionarios, 20% dos dados dos 90% já processados
def gerar_funcionario(arquivo_pessoas_internas, inserts_funcionarios, arquivo_funcionarios):
    with open(arquivo_pessoas_internas, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Ignora o cabeçalho
        pessoas_90 = list(reader)

    # Embaralhar os dados para garantir aleatoriedade
    random.shuffle(pessoas_90)

    # Calcular a quantidade de 20% dos dados dos 90%
    total_pessoas_90 = len(pessoas_90)
    percentual_20 = int(total_pessoas_90 * 0.2)

    # Separar os 20% dos dados
    pessoas_20 = pessoas_90[:percentual_20]

    # Função para salvar os dados no arquivo SQL
    def salvar_no_sql(pessoas_20):
        with open(inserts_funcionarios, mode='w', encoding='utf-8') as sql_file:
            for row in pessoas_20:
                cpf_pessoa = row[0]
                formacao = gerar_formacao()

                # Gerar o comando SQL de inserção para a tabela FUNCIONARIO
                insert_sql = f"INSERT INTO FUNCIONARIO (CPF_INTERNO, FORMACAO) VALUES ('{cpf_pessoa}', '{formacao}');\n"
                sql_file.write(insert_sql)  # Escrever o comando no arquivo .sql

    # Função para salvar os dados no arquivo CSV
    def salvar_no_csv(pessoas_20, nome_arquivo_csv):
        with open(nome_arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Escrever o cabeçalho
            writer.writerows(pessoas_20)  # Escrever os dados no arquivo CSV

    # Salvar os dados nos respectivos arquivos
    salvar_no_sql(pessoas_20)
    salvar_no_csv(pessoas_20, arquivo_funcionarios)

    print(f"Arquivo SQL gerado: {inserts_funcionarios}")
    print(f"Arquivo CSV dos 20% gerado: {arquivo_funcionarios}")
