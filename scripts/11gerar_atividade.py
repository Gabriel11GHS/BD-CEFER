import random
import csv
from pathlib import Path
from datetime import timedelta
from faker import Faker

NOMES_ATIVIDADES = [
    'Treinamento Funcional', 'Iniciação à Corrida', 'Condicionamento Físico',
    'Ginástica Localizada', 'Fortalecimento Muscular', 'Natação Adulto Iniciante',
    'Natação Adulto Avançado', 'Hidroginástica', 'Yoga e Alongamento', 'Ritmos Dançantes',
    'Vôlei Recreativo', 'Futebol Society Amistoso', 'Karatê (Extensão)', 'Kung Fu (Extensão)'
]
fake = Faker('pt_BR')

# --- Assinatura CORRIGIDA: Aceita DIRETÓRIOS ---
def gerar_atividades(sql_dir: Path, csv_dir: Path, num_registros: int):
    """
    Gera dados fictícios para a tabela ATIVIDADE e salva em arquivos SQL e CSV.
    """
    print(f"Gerando {num_registros} registros para ATIVIDADE...")

    # --- Nomes de arquivo definidos AQUI ---
    sql_output_path = sql_dir / 'upgrade_atividade.sql'
    csv_output_path = csv_dir / 'atividades.csv'

    atividades_data_for_csv = []
    sql_statements = []
    pares_unicos = set()

    max_combinacoes = len(NOMES_ATIVIDADES)
    if num_registros > max_combinacoes:
        print(f"  Aviso: Reduzindo número de atividades para {max_combinacoes} (máximo de nomes únicos).")
        num_registros = max_combinacoes

    nomes_selecionados = random.sample(NOMES_ATIVIDADES, num_registros)

    # --- CORREÇÃO: Adicionado enumerate(start=1) para criar o ID local ---
    for id_atividade_local, nome in enumerate(nomes_selecionados, 1):
        # ... (lógica de data permanece a mesma) ...
        tentativas_data = 0
        while tentativas_data < 10: 
            data_inicio_periodo = fake.date_object()
            par = (nome, data_inicio_periodo)
            if par not in pares_unicos:
                pares_unicos.add(par)
                break
            tentativas_data += 1
        else:
            print(f"  Aviso: Não foi possível gerar data única para a atividade '{nome}'. Pulando.")
            continue

        vagas_limite = random.randint(5, 30)
        data_fim_periodo = data_inicio_periodo + timedelta(days=random.randint(30, 180)) if random.random() > 0.1 else None

        data_inicio_str = data_inicio_periodo.isoformat()
        data_fim_str = data_fim_periodo.isoformat() if data_fim_periodo else ''

        # --- CORREÇÃO: Adicionado id_atividade_local ao CSV ---
        atividades_data_for_csv.append([id_atividade_local, nome, vagas_limite, data_inicio_str, data_fim_str])

        # SQL não precisa do ID (IDENTITY)
        nome_sql = nome.replace("'", "''")
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
            # --- CORREÇÃO: Adicionado ID_ATIVIDADE ao cabeçalho ---
            writer.writerow(['ID_ATIVIDADE', 'NOME', 'VAGAS_LIMITE', 'DATA_INICIO_PERIODO', 'DATA_FIM_PERIODO'])
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