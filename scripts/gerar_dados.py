import subprocess
import sys
from pathlib import Path
import importlib;

PROJECT_ROOT = Path(__file__).parent.parent
SQL_OUTPUT_DIR = PROJECT_ROOT / 'sql' / 'populate_mocked_minimal_db'
CSV_OUTPUT_DIR = PROJECT_ROOT / 'sql' / 'csv'

# Garante que os diretórios existam
SQL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

mod_01 = importlib.import_module(".01gerar_pessoas", package=__package__)
mod_02 = importlib.import_module(".02gerar_interno_usp", package=__package__)
mod_03 = importlib.import_module(".03gerar_funcionario", package=__package__)
mod_04 = importlib.import_module(".04gerar_atribuicoes", package=__package__)
mod_05 = importlib.import_module(".05gerar_restricao", package=__package__)
mod_06 = importlib.import_module(".06gerar_educador_fisico", package=__package__)
mod_07 = importlib.import_module(".07gerar_instalacao", package=__package__)
mod_08 = importlib.import_module(".08gerar_equipamento", package=__package__)
mod_09 = importlib.import_module(".09gerar_doacao_equipamento", package=__package__)
mod_10 = importlib.import_module(".10gerar_reservas", package=__package__)
mod_11 = importlib.import_module(".11gerar_atividade", package=__package__)
mod_12 = importlib.import_module(".12gerar_ocorrencia_semanal", package=__package__)
mod_13 = importlib.import_module(".13gerar_conduz_atividade", package=__package__)
mod_14 = importlib.import_module(".14gerar_participacao_atividade", package=__package__)
mod_15 = importlib.import_module(".15gerar_evento", package=__package__)
mod_16 = importlib.import_module(".16gerar_supervisores_eventos", package=__package__)
mod_17 = importlib.import_module(".17gerar_grupo_extensao", package=__package__)
mod_18 = importlib.import_module(".18gerar_atividade_grupo_extensao", package=__package__)

# Parâmetros globais
NUM_PESSOAS = 100   
NUM_INTERNOS_USP = 60 
NUM_FUNCIONARIOS = 15 
NUM_EDUCADORES = 8   
NUM_INSTALACOES = 15
NUM_EQUIPAMENTOS = 50
NUM_DOACOES = 10 
NUM_ATIVIDADES = 20
NUM_OCORRENCIAS_POR_ATIVIDADE = 3 
NUM_RESERVAS = 40
NUM_PARTICIPACOES = 200
NUM_EVENTOS = 5
NUM_GRUPOS_EXTENSAO = 4

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
grupo_extensao_csv_path = CSV_OUTPUT_DIR / 'grupos_extensao.csv'
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
    
    mod_01.gerar_pessoas(SQL_OUTPUT_DIR, CSV_OUTPUT_DIR, NUM_PESSOAS)
    mod_02.gerar_interno_usp(SQL_OUTPUT_DIR, CSV_OUTPUT_DIR, pessoas_csv_path)
    mod_03.gerar_funcionario(pessoas_internas_csv_path, funcionarios_sql_path, funcionarios_csv_path)
    mod_04.gerar_atribuicoes_funcionario(funcionarios_csv_path, funcionario_atribuicao_sql_path, funcionario_atribuicao_csv_path)
    mod_05.gerar_restricoes_funcionario(funcionarios_csv_path, funcionario_restricao_sql_path, funcionario_restricao_csv_path)
    mod_06.gerar_educadores_fisicos(funcionarios_csv_path, educador_fisico_sql_path, educador_fisico_csv_path)
    mod_07.gerar_instalacoes(SQL_OUTPUT_DIR, CSV_OUTPUT_DIR, NUM_INSTALACOES)
    mod_08.gerar_equipamentos(instalacoes_csv_path, equipamentos_sql_path, equipamentos_csv_path, NUM_EQUIPAMENTOS)
    mod_09.gerar_doacoes(pessoas_restantes_csv_path, equipamentos_csv_path, doacao_equipamento_sql_path, doacao_equipamento_csv_path)
    mod_10.gerar_reservas(pessoas_internas_csv_path, instalacoes_csv_path, reserva_sql_path, reserva_csv_path)
    mod_11.gerar_atividades(SQL_OUTPUT_DIR, CSV_OUTPUT_DIR, NUM_ATIVIDADES)
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
    mod_17.gerar_grupo_extensao(SQL_OUTPUT_DIR, CSV_OUTPUT_DIR, NUM_GRUPOS_EXTENSAO, pessoas_internas_csv_path)
    mod_18.gerar_atividade_grupo_extensao(SQL_OUTPUT_DIR, CSV_OUTPUT_DIR, atividade_csv_path, grupo_extensao_csv_path)


    

if __name__ == "__main__":
    main()
