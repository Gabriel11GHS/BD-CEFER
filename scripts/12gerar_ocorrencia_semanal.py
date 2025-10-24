import random
import csv
from pathlib import Path
from datetime import time # Para gerar horários


NOMES_INSTALACOES_POR_TIPO = {
    'Quadra': ['Quadra Poliesportiva A', 'Quadra Poliesportiva B', 'Quadra de Tênis 1', 'Quadra de Tênis 2', 'Quadra de Peteca', 'Quadra de Areia Vôlei', 'Quadra de Areia Beach Tennis'],
    'Piscina': ['Piscina Olímpica', 'Piscina Recreativa'],
    'Academia': ['Academia Principal', 'Espaço Multifuncional Musculação'],
    'Sala': ['Sala de Dança', 'Sala de Ginástica', 'Sala de Alongamento', 'Salão de Eventos'],
    'Campo': ['Campo de Futebol Principal', 'Campo de Futebol Society'],
    'Vestiário': ['Vestiário Masculino A', 'Vestiário Feminino A', 'Vestiário Masculino B', 'Vestiário Feminino B']
}

# Funções auxiliares para gerar dia e horários (podem vir do script original 12)
def gerar_horario_inicio():
    hora = random.randint(8, 18)
    minuto = random.randint(0, 59)
    return time(hora, minuto)

def gerar_horario_fim(horario_inicio):
    minutos_adicionais = random.randint(30, 90)
    # Cálculo cuidadoso para evitar estouro de hora/minuto
    total_minutos_inicio = horario_inicio.hour * 60 + horario_inicio.minute
    total_minutos_fim = total_minutos_inicio + minutos_adicionais
    hora_fim = min(23, total_minutos_fim // 60) # Limita a 23h
    minuto_fim = total_minutos_fim % 60
    # Garante que fim não seja antes do início, mesmo se passar das 23:59 (improvável aqui)
    horario_fim_obj = time(hora_fim, minuto_fim)
    if horario_fim_obj <= horario_inicio:
         # Se fim for <= inicio (ex: inicio 18:50, duracao 80min -> fim 20:10 OK)
         # Mas se inicio 23:40, duracao 30 min -> fim 00:10 -> retornaria 23:59
         return time(23, 59) # Ajuste simples: limita ao fim do dia
    return horario_fim_obj


def gerar_dia_semana():
    dias = ['SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO'] # Removido Domingo, menos comum
    return random.choice(dias)

def gerar_ocorrencias(
    sql_output_path: Path,
    csv_output_path: Path,
    atividades_csv_path: Path,
    instalacoes_csv_path: Path,
    num_medio_ocorrencias: int
):
    """
    Gera ocorrências semanais para atividades, com lógica semântica de instalação,
    e salva em arquivos SQL e CSV.

    Args:
        sql_output_path: Caminho para o arquivo .sql de saída.
        csv_output_path: Caminho para o arquivo .csv de saída.
        atividades_csv_path: Caminho para o arquivo atividades.csv.
        instalacoes_csv_path: Caminho para o arquivo instalacoes.csv.
        num_medio_ocorrencias: Número médio de ocorrências por atividade.
    """
    print("Gerando dados para OCORRENCIA_SEMANAL (com lógica semântica)...")
    ocorrencias_data_for_csv = []
    sql_statements = []
    ocorrencias_unicas = set() # Garante (ID_ATIVIDADE, ID_INSTALACAO, DIA_SEMANA, HORARIO_INICIO) único

    # --- ETAPA 1: Ler atividades do CSV ---
    atividades_map = {} # Dicionário: {id_atividade: 'Nome da Atividade'}
    try:
        with open(atividades_csv_path, 'r', encoding='utf-8') as f_ativ:
            reader = csv.reader(f_ativ)
            header = next(reader) # Pular cabeçalho
            # Encontra os índices das colunas pelo nome (mais robusto)
            try:
                idx_id_ativ = header.index('ID_ATIVIDADE')
                idx_nome_ativ = header.index('NOME')
            except ValueError:
                print(f"  Erro: Cabeçalhos 'ID_ATIVIDADE' ou 'NOME' não encontrados em {atividades_csv_path}")
                return
            for i, row in enumerate(reader):
                # Assume que ID_ATIVIDADE é sequencial 1, 2, 3... se não estiver no CSV
                id_atividade = int(row[idx_id_ativ]) if row[idx_id_ativ] else i + 1
                atividades_map[id_atividade] = row[idx_nome_ativ]
        if not atividades_map:
            print("  Aviso: Nenhuma atividade encontrada no arquivo CSV.")
            return
    except FileNotFoundError:
        print(f"  Erro: Arquivo de atividades não encontrado em {atividades_csv_path}")
        return
    except Exception as e:
        print(f"  Erro ao ler arquivo de atividades: {e}")
        return

    # --- ETAPA 2: Ler instalações do CSV e categorizar ---
    instalacoes_por_tipo = {} # Dicionário: {'Piscina': [1, 2], 'Quadra': [3, 4], ...}
    todos_ids_instalacoes = []
    try:
        with open(instalacoes_csv_path, 'r', encoding='utf-8') as f_inst:
            reader = csv.reader(f_inst)
            header = next(reader) # Pular cabeçalho
            try:
                idx_id_inst = header.index('ID_INSTALACAO')
                idx_tipo_inst = header.index('TIPO')
            except ValueError:
                 print(f"  Erro: Cabeçalhos 'ID_INSTALACAO' ou 'TIPO' não encontrados em {instalacoes_csv_path}")
                 return
            for i, row in enumerate(reader):
                # Assume que ID_INSTALACAO é sequencial 1, 2, 3... se não estiver no CSV
                id_inst = int(row[idx_id_inst]) if row[idx_id_inst] else i + 1
                tipo = row[idx_tipo_inst]
                todos_ids_instalacoes.append(id_inst)
                if tipo not in instalacoes_por_tipo:
                    instalacoes_por_tipo[tipo] = []
                instalacoes_por_tipo[tipo].append(id_inst)
        if not todos_ids_instalacoes:
            print("  Aviso: Nenhuma instalação encontrada no arquivo CSV.")
            return
    except FileNotFoundError:
        print(f"  Erro: Arquivo de instalações não encontrado em {instalacoes_csv_path}")
        return
    except Exception as e:
        print(f"  Erro ao ler arquivo de instalações: {e}")
        return

    ids_instalacoes_gerais = [id_inst for tipo, ids in instalacoes_por_tipo.items() if tipo != 'Vestiário' for id_inst in ids]
    if not ids_instalacoes_gerais:
        print("  Aviso: Nenhuma instalação geral (não-vestiário) disponível. Usando todas.")
        ids_instalacoes_gerais = todos_ids_instalacoes

    # --- ETAPA 3: Função de Mapeamento Semântico (igual à original) ---
    def get_lista_instalacoes_compativeis(nome_atividade):
        # (A função de mapeamento definida na sua pergunta original entra aqui)
        nome_lower = nome_atividade.lower()
        if 'natação' in nome_lower or 'hidroginástica' in nome_lower:
            return instalacoes_por_tipo.get('Piscina')
        if 'yoga' in nome_lower or 'ginástica' in nome_lower or 'dança' in nome_lower or \
           'alongamento' in nome_lower or 'ritmos' in nome_lower or 'karatê' in nome_lower or \
           'kung fu' in nome_lower or 'capoeira' in nome_lower or 'tai chi' in nome_lower:
            # Pode incluir Academia também, se fizer sentido
            return instalacoes_por_tipo.get('Sala', []) + instalacoes_por_tipo.get('Ginásio', [])
        if 'funcional' in nome_lower or 'muscular' in nome_lower or 'condicionamento' in nome_lower or 'musculação' in nome_lower:
             # Pode incluir Sala ou Espaço Multifuncional
            return instalacoes_por_tipo.get('Academia', []) + instalacoes_por_tipo.get('Espaço Multifuncional', []) + instalacoes_por_tipo.get('Sala', [])
        if 'futebol' in nome_lower:
            return instalacoes_por_tipo.get('Campo')
        if 'vôlei' in nome_lower or 'futsal' in nome_lower or 'basquete' in nome_lower or \
           'tênis' in nome_lower or 'peteca' in nome_lower or 'beach tennis' in nome_lower or 'handebol' in nome_lower:
            # Pode incluir Ginásio também
            return instalacoes_por_tipo.get('Quadra', []) + instalacoes_por_tipo.get('Ginásio', [])
        if 'corrida' in nome_lower or 'atletismo' in nome_lower or 'caminhada' in nome_lower:
             return instalacoes_por_tipo.get('Pista de Atletismo') # Assumindo que existe esse tipo
        # Adicione mais mapeamentos conforme necessário
        return None # Retorna None para usar a lista geral

    # --- ETAPA 4: Gerar Ocorrências ---
    for id_atividade, nome_atividade in atividades_map.items():
        num_ocorrencias_para_ativ = max(1, random.randint(num_medio_ocorrencias - 1, num_medio_ocorrencias + 2)) # Varia um pouco

        lista_instalacoes_candidatas = get_lista_instalacoes_compativeis(nome_atividade)

        # Se não houver mapeamento específico ou a lista específica estiver vazia, usa a geral
        if not lista_instalacoes_candidatas:
            lista_instalacoes_usar = ids_instalacoes_gerais
        else:
            lista_instalacoes_usar = lista_instalacoes_candidatas

        if not lista_instalacoes_usar: # Último fallback, se nem a geral tiver algo
             print(f"  Aviso: Nenhuma instalação compatível ou geral encontrada para '{nome_atividade}'. Pulando.")
             continue

        for _ in range(num_ocorrencias_para_ativ):
            tentativas_unicas = 0
            while tentativas_unicas < 20: # Tenta gerar uma ocorrência única
                id_instalacao = random.choice(lista_instalacoes_usar)
                dia_semana = gerar_dia_semana()
                horario_inicio = gerar_horario_inicio()
                chave_unica = (id_atividade, id_instalacao, dia_semana, horario_inicio)

                if chave_unica not in ocorrencias_unicas:
                    ocorrencias_unicas.add(chave_unica)
                    horario_fim = gerar_horario_fim(horario_inicio)

                    # Formata para CSV e SQL
                    horario_inicio_str = horario_inicio.strftime('%H:%M:%S')
                    horario_fim_str = horario_fim.strftime('%H:%M:%S')

                    ocorrencias_data_for_csv.append([id_atividade, id_instalacao, dia_semana, horario_inicio_str, horario_fim_str])

                    sql = (
                        f"INSERT INTO OCORRENCIA_SEMANAL (ID_ATIVIDADE, ID_INSTALACAO, DIA_SEMANA, HORARIO_INICIO, HORARIO_FIM) "
                        f"VALUES ({id_atividade}, {id_instalacao}, '{dia_semana}', '{horario_inicio_str}', '{horario_fim_str}');"
                    )
                    sql_statements.append(sql)
                    break # Sai do while de tentativas_unicas
            else:
                 print(f"  Aviso: Não foi possível gerar ocorrência única para atividade ID {id_atividade} após 20 tentativas.")


    # Escreve CSV
    try:
        with open(csv_output_path, 'w', newline='', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)
            # ID_OCORRENCIA não é incluído, pois será gerado pelo BD
            writer.writerow(['ID_ATIVIDADE', 'ID_INSTALACAO', 'DIA_SEMANA', 'HORARIO_INICIO', 'HORARIO_FIM'])
            writer.writerows(ocorrencias_data_for_csv)
        print(f"  Arquivo CSV gerado com sucesso em: {csv_output_path}")
    except Exception as e:
        print(f"  Erro ao gerar arquivo CSV para OCORRENCIA_SEMANAL: {e}")
        return

    # Escreve SQL
    try:
        with open(sql_output_path, 'w', encoding='utf-8') as file_sql:
            for statement in sql_statements:
                file_sql.write(statement + '\n')
        print(f"  Arquivo SQL gerado com sucesso em: {sql_output_path}")
        print(f"  Total de {len(sql_statements)} ocorrências geradas.")
    except Exception as e:
        print(f"  Erro ao gerar arquivo SQL para OCORRENCIA_SEMANAL: {e}")