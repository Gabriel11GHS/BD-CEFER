import subprocess
import sys
from pathlib import Path
import importlib;

mod_01 = importlib.import_module("dados_ficticios.01gerar_pessoas")
mod_02 = importlib.import_module("dados_ficticios.02gerar_interno_usp")
mod_03 = importlib.import_module("dados_ficticios.03gerar_funcionario")
mod_04 = importlib.import_module("dados_ficticios.04gerar_atribuicoes")
mod_05 = importlib.import_module("dados_ficticios.05gerar_restricao")
mod_06 = importlib.import_module("dados_ficticios.06gerar_educador_fisico")
mod_07 = importlib.import_module("dados_ficticios.07gerar_instalacao")
mod_08 = importlib.import_module("dados_ficticios.08gerar_equipamento")
mod_09 = importlib.import_module("dados_ficticios.09gerar_doacao_equipamento")
mod_10 = importlib.import_module("dados_ficticios.10gerar_reservas")
mod_11 = importlib.import_module("dados_ficticios.11gerar_atividade")
mod_12 = importlib.import_module("dados_ficticios.12gerar_ocorrencia_semanal")
mod_13 = importlib.import_module("dados_ficticios.13gerar_conduz_atividade")
mod_14 = importlib.import_module("dados_ficticios.14gerar_participacao_atividade")
mod_15 = importlib.import_module("dados_ficticios.15gerar_evento")
mod_16 = importlib.import_module("dados_ficticios.16gerar_supervisores_eventos")
mod_17 = importlib.import_module("dados_ficticios.17gerar_grupo_extensao")
mod_18 = importlib.import_module("dados_ficticios.18gerar_atividade_grupo_extensao")

# Lista de scripts que você quer executar
scripts = [
    "01gerar_pessoas.py",
    "02gerar_interno_usp.py",
    "03gerar_funcionario.py",
    "04gerar_atribuicoes.py",
    "05gerar_restricao.py",
    "06gerar_educador_fisico.py",
    "07gerar_instalacao.py",
    "08gerar_equipamento.py",
    "09gerar_doacao_equipamento.py",
    "10gerar_reservas.py",
    "11gerar_atividade.py",
    "12gerar_ocorrencia_semanal.py",
    "13gerar_conduz_atividade.py",
    "14gerar_participacao_atividade.py",
    "15gerar_evento.py",
    "16gerar_supervisores_eventos.py",
    "17gerar_grupo_extensao.py",
    "18gerar_atividade_grupo_extensao.py"
]

for script in scripts:
    print(f"Rodando {script}...")
    # subprocess.run garante que você espere o script terminar antes de continuar
    subprocess.run([sys.executable, script], check=True)
    print(f"{script} concluído.\n")

# Parâmetros globais
NUM_PESSOAS = 100   
NUM_INTERNOS_USP = 60 # Deve ser <= NUM_PESSOAS
NUM_FUNCIONARIOS = 15 # Deve ser <= NUM_INTERNOS_USP
NUM_EDUCADORES = 8   # Deve ser <= NUM_FUNCIONARIOS
NUM_INSTALACOES = 15
NUM_EQUIPAMENTOS = 50
NUM_DOACOES = 10     # Deve ser <= NUM_EQUIPAMENTOS e <= NUM_PESSOAS
NUM_ATIVIDADES = 20
NUM_OCORRENCIAS_POR_ATIVIDADE = 3 # Média
NUM_RESERVAS = 40
NUM_PARTICIPACOES = 200
NUM_EVENTOS = 5
NUM_GRUPOS_EXTENSAO = 4

# Diretórios de saída
PROJECT_ROOT = Path(__file__).parent
SQL_OUTPUT_DIR = PROJECT_ROOT / 'sql' / 'populate_mocked_minimal_db'
CSV_OUTPUT_DIR = PROJECT_ROOT / 'sql' / 'csv'

SQL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Saída CSV
pessoas_csv_path = CSV_OUTPUT_DIR / 'pessoas.csv'
pessoas_internas_csv_path = CSV_OUTPUT_DIR / 'pessoas_internas.csv'
pessoas_restantes_csv_path = CSV_OUTPUT_DIR / 'pessoas_restantes.csv'
funcionarios_csv_path = CSV_OUTPUT_DIR / 'funcionarios.csv'
funcionario_atribuicao_csv_path = CSV_OUTPUT_DIR / 'funcionario_atribuicao.csv'
funcionario_restricao_csv_path = CSV_OUTPUT_DIR / 'funcionario_restricao.csv'
educador_fisico_csv_path = CSV_OUTPUT_DIR / 'educadores_fisicos.csv'
instalacoes_csv_path = CSV_OUTPUT_DIR / 'instalacoes.csv'
equipamentos_csv_path = CSV_OUTPUT_DIR / 'equipamentos.csv'
doacao_equipamento_csv_path = CSV_OUTPUT_DIR / 'doacao_equipamento.csv'
reserva_csv_path = CSV_OUTPUT_DIR / 'reservas.csv'
atividade_csv_path = CSV_OUTPUT_DIR / 'atividades.csv'
ocorrencia_semanal_csv_path = CSV_OUTPUT_DIR / 'ocorrencias_semanais.csv'
conduz_atividade_csv_path = CSV_OUTPUT_DIR / 'conduz_atividade.csv'
participacao_atividade_csv_path = CSV_OUTPUT_DIR / 'participacao_atividade.csv'
evento_csv_path = CSV_OUTPUT_DIR / 'eventos.csv'
supervisao_evento_csv_path = CSV_OUTPUT_DIR / 'supervisao_evento.csv'
grupo_extensao_csv_path = CSV_OUTPUT_DIR / 'grupo_extensao.csv'
atividade_grupo_extensao_csv_path = CSV_OUTPUT_DIR / 'atividade_grupo_extensao.csv'

#Saída SQL
pessoas_sql_path = SQL_OUTPUT_DIR / 'upgrade_pessoa.sql'
pessoas_internas_sql_path = SQL_OUTPUT_DIR / 'upgrade_interno_usp.sql'
funcionarios_sql_path = SQL_OUTPUT_DIR / 'upgrade_funcionario.sql'
funcionario_atribuicao_sql_path = SQL_OUTPUT_DIR / 'upgrade_funcionario_atribuicao.sql'
funcionario_restricao_sql_path = SQL_OUTPUT_DIR / 'upgrade_funcionario_restricao.sql'
educador_fisico_sql_path = SQL_OUTPUT_DIR / 'upgrade_educador_fisico.sql'
instalacoes_sql_path = SQL_OUTPUT_DIR / 'upgrade_instalacao.sql'
equipamentos_sql_path = SQL_OUTPUT_DIR / 'upgrade_equipamento.sql'
doacao_equipamento_sql_path = SQL_OUTPUT_DIR / 'upgrade_doacao.sql'
reserva_sql_path = SQL_OUTPUT_DIR / 'upgrade_reserva.sql'
atividade_sql_path = SQL_OUTPUT_DIR / 'upgrade_atividade.sql'
ocorrencia_semanal_sql_path = SQL_OUTPUT_DIR / 'upgrade_ocorrencia_semanal.sql'
conduz_atividade_sql_path = SQL_OUTPUT_DIR / 'upgrade_conduz_atividade.sql'
participacao_atividade_sql_path = SQL_OUTPUT_DIR / 'upgrade_participacao_atividade.sql'
evento_sql_path = SQL_OUTPUT_DIR / 'upgrade_evento.sql'
supervisao_evento_sql_path = SQL_OUTPUT_DIR / 'upgrade_supervisao_evento.sql'
grupo_extensao_sql_path = SQL_OUTPUT_DIR / 'upgrade_grupo_extensao.sql'
atividade_grupo_extensao_sql_path = SQL_OUTPUT_DIR / 'upgrade_atividade_grupo_extensao.sql'

def main():
    
    mod_01.gerar_pessoas(pessoas_csv_path, pessoas_sql_path, NUM_PESSOAS)
    mod_02.gerar_interno_usp(pessoas_csv_path, pessoas_internas_sql_path, pessoas_internas_csv_path, 'pessoas_restantes_csv_path')
    mod_03.gerar_funcionario(pessoas_internas_csv_path, funcionarios_sql_path, funcionarios_csv_path)
    mod_04.gerar_atribuicoes(funcionarios_csv_path, funcionario_atribuicao_sql_path, funcionario_atribuicao_csv_path)
    mod_05.gerar_restricao(funcionarios_csv_path, funcionario_restricao_sql_path, funcionario_restricao_csv_path)
    mod_06.gerar_educadores_fisicos(funcionarios_csv_path, educador_fisico_sql_path, educador_fisico_csv_path)
    mod_07.gerar_instalacoes(instalacoes_sql_path, instalacoes_csv_path, NUM_INSTALACOES)
    mod_08.gerar_equipamentos(instalacoes_csv_path, equipamentos_sql_path, equipamentos_csv_path, NUM_EQUIPAMENTOS)
    mod_09.gerar_doacao_equipamento(pessoas_restantes_csv_path, equipamentos_csv_path, doacao_equipamento_sql_path, doacao_equipamento_csv_path)
    mod_10.gerar_reservas(pessoas_internas_csv_path, instalacoes_csv_path, reserva_sql_path, reserva_csv_path)
    mod_11.gerar_atividades(atividade_sql_path, atividade_csv_path, NUM_ATIVIDADES)
    mod_12.gerar_ocorrencias(ocorrencia_semanal_sql_path, ocorrencia_semanal_csv_path, atividade_csv_path, instalacoes_csv_path, NUM_OCORRENCIAS_POR_ATIVIDADE)
    mod_13.gerar_conduz_atividade(conduz_atividade_sql_path, conduz_atividade_csv_path, educador_fisico_csv_path, atividade_csv_path)
    mod_14.gerar_participacao_atividade(
        participacao_atividade_sql_path,
        participacao_atividade_csv_path,
        pessoas_restantes_csv_path,
        pessoas_internas_csv_path,
        atividade_csv_path
    )
    mod_15.gerar_eventos(reserva_csv_path, evento_sql_path, evento_csv_path)
    mod_16.gerar_supervisores_evento(funcionario_atribuicao_csv_path, evento_csv_path, supervisao_evento_sql_path, supervisao_evento_csv_path)
    mod_17.gerar_grupo_extensao(grupo_extensao_sql_path, grupo_extensao_csv_path, NUM_GRUPOS_EXTENSAO, pessoas_internas_csv_path)
    mod_18.gerar_atividade_grupo_extensao(atividade_csv_path, grupo_extensao_csv_path, atividade_grupo_extensao_sql_path, atividade_grupo_extensao_csv_path)

if __name__ == "__main__":
    
    main()
