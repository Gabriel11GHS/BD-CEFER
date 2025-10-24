import random
import csv
from datetime import datetime, timedelta

# Funções auxiliares
def gerar_data_inicial():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

def gerar_data_fim(data_inicio):
    tipo_periodo = random.choice(['bimestral', 'semestral'])
    if tipo_periodo == 'bimestral':
        delta = random.randint(30, 60)
    else:
        delta = random.randint(90, 180)
    return data_inicio + timedelta(days=delta)

def gerar_nome_atividade():
    atividades = [
        "Futebol", "Basquete", "Vôlei", "Natação", "Caminhada", "Yoga", "Pilates", "CrossFit",
        "Musculação", "Tênis", "Judô", "Karate", "Jiu-Jitsu", "Boxe", "Zumba", "Dança",
        "Ciclismo", "Atletismo", "Handebol", "Tiro com arco", "Esgrima", "Trekking", "Skate",
        "Ginástica", "Escalada", "Luta livre", "Capoeira", "Judo", "Surf", "Badminton", "Bicicross"
    ]
    return random.choice(atividades)

# Gerar atividades
def gerar_atividades(nome_arquivo_sql, nome_arquivo_csv, quantidade=100):
    atividades = []
    atividades_set = set()
    id_counter = 1

    while len(atividades) < quantidade:
        nome_atividade = gerar_nome_atividade()
        data_inicio = gerar_data_inicial()
        key = (nome_atividade, data_inicio)
        if key in atividades_set:
            continue
        atividades_set.add(key)

        vagas_limite = random.randint(10, 30)
        data_fim = gerar_data_fim(data_inicio)

        atividades.append([id_counter, nome_atividade, vagas_limite, data_inicio, data_fim])
        id_counter += 1

    # SQL
    with open(nome_arquivo_sql, 'w', encoding='utf-8') as sql_file:
        for atividade in atividades:
            insert_sql = (
                f"INSERT INTO ATIVIDADE (ID_ATIVIDADE, NOME, VAGAS_LIMITE, DATA_INICIO_PERIODO, DATA_FIM_PERIODO) "
                f"VALUES ({atividade[0]}, '{atividade[1]}', {atividade[2]}, '{atividade[3]}', '{atividade[4]}');\n"
            )
            sql_file.write(insert_sql)

    # CSV
    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_ATIVIDADE', 'NOME', 'VAGAS_LIMITE', 'DATA_INICIO_PERIODO', 'DATA_FIM_PERIODO'])
        writer.writerows(atividades)

    print(f"Arquivo SQL de atividades gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV de atividades gerado: {nome_arquivo_csv}")

# Exemplo de uso
gerar_atividades('upgrade_atividade.sql', 'atividades.csv', quantidade=100)
