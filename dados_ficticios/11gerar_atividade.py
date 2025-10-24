import random
import csv
from pathlib import Path
from datetime import timedelta
from faker import Faker # Necessário importar Faker se 'fake' for usado

# Exemplo:
NOMES_ATIVIDADES = [
    'Treinamento Funcional', 'Iniciação à Corrida', 'Condicionamento Físico',
    'Ginástica Localizada', 'Fortalecimento Muscular', 'Natação Adulto Iniciante',
    'Natação Adulto Avançado', 'Hidroginástica', 'Yoga e Alongamento', 'Ritmos Dançantes',
    'Vôlei Recreativo', 'Futebol Society Amistoso', 'Karatê (Extensão)', 'Kung Fu (Extensão)'
]
fake = Faker('pt_BR') # Instanciar Faker

def gerar_atividades(sql_output_path: Path, csv_output_path: Path, num_registros: int):
    """
    Gera dados fictícios para a tabela ATIVIDADE e salva em arquivos SQL e CSV.

    Args:
        sql_output_path: Caminho completo (objeto Path) para o arquivo .sql de saída.
        csv_output_path: Caminho completo (objeto Path) para o arquivo .csv de saída.
        num_registros: Quantidade de atividades a serem geradas.
    """
    print(f"Gerando {num_registros} registros para ATIVIDADE...")
    atividades_data_for_csv = [] # Lista para dados do CSV
    sql_statements = [] # Lista para comandos SQL
    pares_unicos = set() # Garante (NOME, DATA_INICIO_PERIODO) único

    # Limita o número de registros ao total de nomes de atividades disponíveis
    max_combinacoes = len(NOMES_ATIVIDADES)
    if num_registros > max_combinacoes:
        print(f"  Aviso: Reduzindo número de atividades para {max_combinacoes} (máximo de nomes únicos).")
        num_registros = max_combinacoes

    # Usa 'random.sample' para garantir nomes únicos
    nomes_selecionados = random.sample(NOMES_ATIVIDADES, num_registros)

    for nome in nomes_selecionados:
        tentativas_data = 0
        while tentativas_data < 10: 
            data_inicio_periodo = fake.date_object() # Usando date_object() para obter um objeto date
            par = (nome, data_inicio_periodo)

            if par not in pares_unicos:
                pares_unicos.add(par)
                break
            tentativas_data += 1
        else:
            # Se não conseguiu data única após tentativas, pula este nome
            print(f"  Aviso: Não foi possível gerar data única para a atividade '{nome}'. Pulando.")
            continue

        vagas_limite = random.randint(5, 30)
        # Data fim pode ser NULL ou uma data futura
        data_fim_periodo = data_inicio_periodo + timedelta(days=random.randint(30, 180)) if random.random() > 0.1 else None # 10% chance de ser NULL

        # Dados para CSV (sem ID)
        # Converte datas para string ISO para o CSV
        data_inicio_str = data_inicio_periodo.isoformat()
        data_fim_str = data_fim_periodo.isoformat() if data_fim_periodo else '' # String vazia para NULL no CSV
        atividades_data_for_csv.append([nome, vagas_limite, data_inicio_str, data_fim_str])

        # Comando SQL (sem ID_ATIVIDADE)
        nome_sql = nome.replace("'", "''")
        # Formata data_fim para SQL (NULL ou 'YYYY-MM-DD')
        data_fim_sql = f"'{data_fim_periodo.isoformat()}'" if data_fim_periodo else "NULL"

        sql = (
            f"INSERT INTO ATIVIDADE (NOME, VAGAS_LIMITE, DATA_INICIO_PERIODO, DATA_FIM_PERIODO) "
            f"VALUES ('{nome_sql}', {vagas_limite}, '{data_inicio_periodo.isoformat()}', {data_fim_sql});"
        )
        sql_statements.append(sql)

    # Escreve o arquivo CSV
    try:
        with open(csv_output_path, 'w', newline='', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)
            # Cabeçalho adaptado (sem ID)
            writer.writerow(['NOME', 'VAGAS_LIMITE', 'DATA_INICIO_PERIODO', 'DATA_FIM_PERIODO'])
            writer.writerows(atividades_data_for_csv)
        print(f"  Arquivo CSV gerado com sucesso em: {csv_output_path}")
    except Exception as e:
        print(f"  Erro ao gerar arquivo CSV para ATIVIDADE: {e}")
        return

    # Escreve o arquivo SQL
    try:
        with open(sql_output_path, 'w', encoding='utf-8') as file_sql:
            for statement in sql_statements:
                file_sql.write(statement + '\n')
        print(f"  Arquivo SQL gerado com sucesso em: {sql_output_path}")
    except Exception as e:
        print(f"  Erro ao gerar arquivo SQL para ATIVIDADE: {e}")