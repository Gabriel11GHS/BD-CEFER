import csv
from faker import Faker
import random
from pathlib import Path

# Função para gerar CPF válido
def gerar_cpf():
    def calcular_dv(cpf_base):
        cpf_base = [int(d) for d in cpf_base]
        for i in range(2):
            peso = list(range(10 - i, 1, -1)) if i == 0 else list(range(11 - i, 1, -1))
            soma = sum([cpf_base[j] * peso[j] for j in range(len(peso))])
            resto = soma % 11
            digito = 0 if resto < 2 else 11 - resto
            cpf_base.append(digito)
        return ''.join(map(str, cpf_base))

    while True:
        cpf_base = [str(random.randint(0, 9)) for _ in range(9)]
        cpf = calcular_dv(cpf_base)
        if cpf[0] != '0':  # opcional, evitar CPF começando com 0
            return cpf

# Inicializa Faker
fake = Faker('pt_BR')

def gerar_pessoas(sql_dir: Path, csv_dir: Path, quantidade):

    nome_arquivo_csv = csv_dir / 'pessoas.csv'
    nome_arquivo_sql = sql_dir / 'upgrade_pessoa.sql'

    cpfs_gerados = set()  # Garante CPFs únicos
    emails_usados = set()  # Garante emails únicos

    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as file_csv, \
         open(nome_arquivo_sql, 'w', encoding='utf-8') as file_sql:
        
        writer_csv = csv.writer(file_csv)
        writer_csv.writerow(['CPF', 'NOME', 'EMAIL', 'CELULAR', 'DATA_NASCIMENTO'])

        for _ in range(quantidade):
            # Gera CPF único
            cpf = gerar_cpf()
            while cpf in cpfs_gerados:
                cpf = gerar_cpf()
            cpfs_gerados.add(cpf)

            nome = fake.name()

            # Gera email único
            email = fake.email()
            while email in emails_usados:
                email = fake.email()
            emails_usados.add(email)

            celular = f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)

            writer_csv.writerow([cpf, nome, email, celular, data_nascimento])

            insert_sql = f"INSERT INTO PESSOA (CPF, NOME, EMAIL, CELULAR, DATA_NASCIMENTO) " \
                         f"VALUES ('{cpf}', '{nome.replace('\'','\'\'')}', '{email}', '{celular}', '{data_nascimento}');\n"
            file_sql.write(insert_sql)

    print(f"CSV gerado com sucesso em: {nome_arquivo_csv}")
    print(f"SQL gerado com sucesso em: {nome_arquivo_sql}")
