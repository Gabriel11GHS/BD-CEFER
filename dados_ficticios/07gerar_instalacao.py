import csv
import random

# Função para gerar o nome da instalação (exemplo)
def gerar_nome_instalacao():
    nomes = [
        "Ginásio Principal", "Quadra de Vôlei", "Piscina Olímpica", "Sala de Musculação", 
        "Campo de Futebol", "Sala de Yoga", "Pista de Atletismo", "Campo de Basquete", 
        "Sala de Dança", "Quadra de Tênis"
    ]
    return nomes  # Retorna lista para combinar sem repetição

# Função para gerar o tipo de instalação
def gerar_tipo_instalacao():
    tipos = ["Ginásio", "Quadra de Vôlei", "Piscina", "Sala de Musculação", "Campo de Futebol", 
             "Sala de Yoga", "Pista de Atletismo", "Campo de Basquete", "Sala de Dança", "Quadra de Tênis"]
    return tipos  # Retorna lista para combinar sem repetição

# Função para gerar a capacidade da instalação
def gerar_capacidade():
    return random.randint(10, 200)  # Capacidade entre 10 e 200

# Função para determinar se a instalação é reservável (S ou N)
def gerar_reservavel():
    return random.choice(['S', 'N'])

# Função para gerar instalações únicas
def gerar_instalacoes():
    nomes = gerar_nome_instalacao()
    tipos = gerar_tipo_instalacao()
    
    combinacoes_possiveis = [(n, t) for n in nomes for t in tipos]  # Todas as combinações possíveis
    random.shuffle(combinacoes_possiveis)  # Aleatorizar a ordem
    
    # Escolher 30 combinações únicas
    escolhidas = combinacoes_possiveis[:30]
    
    instalacoes = []
    for idx, (nome, tipo) in enumerate(escolhidas, start=1):  # ID_INSTALACAO a partir de 1
        capacidade = gerar_capacidade()
        reservavel = gerar_reservavel()
        instalacoes.append([idx, nome, tipo, capacidade, reservavel])  # Adiciona ID_INSTALACAO
    
    # Gerar o SQL
    with open('upgrade_instalacao.sql', 'w', encoding='utf-8') as sql_file:
        for id_inst, nome, tipo, capacidade, reservavel in instalacoes:
            insert_sql = f"INSERT INTO INSTALACAO (ID_INSTALACAO, NOME, TIPO, CAPACIDADE, EH_RESERVAVEL) VALUES ({id_inst}, '{nome}', '{tipo}', {capacidade}, '{reservavel}');\n"
            sql_file.write(insert_sql)

    # Gerar o CSV
    with open('instalacoes.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_INSTALACAO', 'NOME', 'TIPO', 'CAPACIDADE', 'EH_RESERVAVEL'])
        writer.writerows(instalacoes)


    print("Arquivo SQL de instalações gerado: upgrade_instalacao.sql")
    print("Arquivo CSV de instalações gerado: instalacoes.csv")

# Exemplo de uso:
gerar_instalacoes()
