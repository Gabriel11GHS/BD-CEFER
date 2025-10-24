import sys
import os
import random
from datetime import date, timedelta, time
from decimal import Decimal

# Adiciona o diretório raiz do projeto ao PYTHONPATH
# para permitir a importação de 'src.dbsession'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    # Tenta importar as dependências
    from faker import Faker
    from src.dbsession import DBSession # Importa sua classe
except ImportError as e:
    print(f"Erro: Biblioteca necessária não encontrada: {e}")
    print("Por favor, ative seu ambiente virtual e instale as dependências com:")
    print("source env/bin/activate")
    print("pip install -r requirements.txt")
    sys.exit(1)

# --- Configurações ---
SCHEMA = "tests" # Ou o schema que você está usando para desenvolvimento/teste
fake = Faker('pt_BR')

# --- Quantidade de Dados a Gerar ---
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


# --- Listas de Dados Específicos do CEFER ---
CATEGORIAS_INTERNO_USP = ['ALUNO_GRADUACAO', 'ALUNO_MESTRADO', 'ALUNO_DOUTORADO', 'FUNCIONARIO']
FORMACOES_FUNCIONARIO = ['Educação Física', 'Administração', 'Fisioterapia', 'Nutrição', 'Gestão Esportiva', 'Serviço Social']
ATRIBUICOES_FUNCIONARIO = ['Secretaria', 'Manutenção', 'Limpeza', 'Instrutor', 'Coordenação', 'Supervisão', 'Gestão']
RESTRICOES_FISICAS = ['Alergia a Cloro', 'Problema na Coluna', 'Lesão no Joelho', 'Asma', 'Hipertensão']
TIPOS_INSTALACAO = ['Quadra', 'Piscina', 'Academia', 'Sala', 'Campo', 'Vestiário']
NOMES_INSTALACAO_POR_TIPO = {
    'Quadra': ['Quadra Poliesportiva A', 'Quadra Poliesportiva B', 'Quadra de Tênis 1', 'Quadra de Tênis 2', 'Quadra de Peteca', 'Quadra de Areia Vôlei', 'Quadra de Areia Beach Tennis'],
    'Piscina': ['Piscina Olímpica', 'Piscina Recreativa'],
    'Academia': ['Academia Principal', 'Espaço Multifuncional Musculação'],
    'Sala': ['Sala de Dança', 'Sala de Ginástica', 'Sala de Alongamento', 'Salão de Eventos'],
    'Campo': ['Campo de Futebol Principal', 'Campo de Futebol Society'],
    'Vestiário': ['Vestiário Masculino A', 'Vestiário Feminino A', 'Vestiário Masculino B', 'Vestiário Feminino B']
}
NOMES_EQUIPAMENTOS = [
    'Esteira Elétrica', 'Bicicleta Ergométrica', 'Halteres 5kg', 'Halteres 10kg', 'Anilhas 20kg',
    'Bola de Vôlei', 'Bola de Basquete', 'Bola de Futebol', 'Rede de Vôlei', 'Rede de Tênis',
    'Raquete de Tênis', 'Raquete de Tênis de Mesa', 'Bolinha de Tênis de Mesa', 'Pé de Pato Natação',
    'Prancha Natação', 'Boia Espaguete', 'Colchonete Ginástica', 'Bola de Pilates', 'Cama Elástica Jump', 'Kit Primeiros Socorros'
]
NOMES_ATIVIDADES = [
    'Treinamento Funcional', 'Iniciação à Corrida', 'Condicionamento Físico',
    'Ginástica Localizada', 'Fortalecimento Muscular', 'Natação Adulto Iniciante',
    'Natação Adulto Avançado', 'Hidroginástica', 'Yoga e Alongamento', 'Ritmos Dançantes',
    'Vôlei Recreativo', 'Futebol Society Amistoso', 'Karatê (Extensão)', 'Kung Fu (Extensão)'
]
DIAS_SEMANA = ['SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO', 'DOMINGO']
NOMES_EVENTOS = ['Campeonato Interno de Futsal', 'Festival de Ginástica Artística', 'Corrida Rústica USP', 'Aula Aberta de Yoga', 'Torneio de Tênis de Mesa']
NOMES_GRUPOS_EXTENSAO = ['Grupo de Karatê Shotokan', 'Equipe Kung Fu Garra de Águia', 'Grupo de Estudos Tai Chi Chuan', 'Projeto Capoeira Angola']

# --- Funções de População ---

def limpar_tabelas(cursor):
    """Limpa todas as tabelas na ordem inversa de dependência para evitar erros de FK."""
    print("Limpando tabelas...")
    tabelas_ordem_inversa = [
        'ATIVIDADE_GRUPO_EXTENSAO', 'SUPERVISAO_EVENTO', 'EVENTO',
        'PARTICIPACAO_ATIVIDADE', 'CONDUZ_ATIVIDADE', 'OCORRENCIA_SEMANAL',
        'ATIVIDADE', 'RESERVA', 'DOACAO', 'EQUIPAMENTO', 'INSTALACAO',
        'EDUCADOR_FISICO', 'FUNCIONARIO_RESTRICAO', 'FUNCIONARIO_ATRIBUICAO',
        'FUNCIONARIO', 'GRUPO_EXTENSAO', 'INTERNO_USP', 'PESSOA'
    ]
    try:
        for tabela in tabelas_ordem_inversa:
            print(f"  Limpando {tabela}...")
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = %s AND table_name = lower(%s)
                );
            """, (SCHEMA, tabela))
            if cursor.fetchone()[0]:
                cursor.execute(f"TRUNCATE TABLE {SCHEMA}.{tabela} RESTART IDENTITY CASCADE;")
            else:
                 print(f"  Aviso: Tabela {tabela} não encontrada no schema {SCHEMA}.")
        print("Tabelas limpas com sucesso.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"Erro ao limpar tabelas: {e}")
        raise 

def popular_pessoa(cursor, num_registros):
    print(f"Populando PESSOA com {num_registros} registros...")
    pessoas_data = []
    cpfs_gerados = set()
    while len(pessoas_data) < num_registros:
        cpf = fake.unique.cpf().replace('.', '').replace('-', '') 
        if cpf not in cpfs_gerados:
            nome = fake.name()
            email = fake.unique.email()
            celular = fake.phone_number() 
            data_nasc = fake.date_of_birth(minimum_age=15, maximum_age=80)
            pessoas_data.append((cpf, nome, email, celular, data_nasc))
            cpfs_gerados.add(cpf)

    sql = """
        INSERT INTO PESSOA (CPF, NOME, EMAIL, CELULAR, DATA_NASCIMENTO)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(sql, pessoas_data)
        print(f"  Inseridos {len(pessoas_data)} registros em PESSOA.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro ao inserir em PESSOA: {e}")
        return []
    return list(cpfs_gerados)

def popular_interno_usp(cursor, cpfs_disponiveis, num_registros):
    print(f"Populando INTERNO_USP com {num_registros} registros...")
    if not cpfs_disponiveis or num_registros == 0:
        print("  Aviso: Não há CPFs disponíveis ou num_registros é 0 para INTERNO_USP.")
        return [], {}

    internos_data = []
    num_a_selecionar = min(num_registros, len(cpfs_disponiveis))
    cpfs_selecionados = random.sample(cpfs_disponiveis, num_a_selecionar)
    internos_por_categoria = {cat: [] for cat in CATEGORIAS_INTERNO_USP}

    for cpf in cpfs_selecionados:
        nusp = None
        while nusp is None: # Tenta gerar NUSP único (simplificado)
             try:
                 nusp = str(fake.unique.random_number(digits=8, fix_len=True)) # Ajuste o número de dígitos
             except: # Pode falhar se esgotar, tenta de novo
                 fake.unique.clear() # Limpa para tentar novamente
                 nusp = None
                 print("  Aviso: Limpando cache unique para NUSP.")
        categoria = random.choice(CATEGORIAS_INTERNO_USP)
        internos_data.append((cpf, nusp, categoria))
        internos_por_categoria[categoria].append(cpf)

    sql = """
        INSERT INTO INTERNO_USP (CPF_PESSOA, NUSP, CATEGORIA)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.executemany(sql, internos_data)
        print(f"  Inseridos {len(internos_data)} registros em INTERNO_USP.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em INTERNO_USP: {e}")
        return [], {}
    # Retorna a lista total de CPFs de internos E um dicionário com CPFs por categoria
    return cpfs_selecionados, internos_por_categoria

def popular_funcionario(cursor, cpfs_funcionarios_disponiveis):
    num_registros = len(cpfs_funcionarios_disponiveis)
    print(f"Populando FUNCIONARIO com {num_registros} registros...")
    if not cpfs_funcionarios_disponiveis:
        print("  Aviso: Não há CPFs de funcionários disponíveis.")
        return []

    funcionarios_data = []
    for cpf in cpfs_funcionarios_disponiveis:
        formacao = random.choice(FORMACOES_FUNCIONARIO + [None]) # Permite formação nula
        funcionarios_data.append((cpf, formacao))

    sql = "INSERT INTO FUNCIONARIO (CPF_INTERNO, FORMACAO) VALUES (%s, %s)"
    try:
        cursor.executemany(sql, funcionarios_data)
        print(f"  Inseridos {len(funcionarios_data)} registros em FUNCIONARIO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em FUNCIONARIO: {e}")
        return []
    return cpfs_funcionarios_disponiveis # Retorna os mesmos CPFs

def popular_educador_fisico(cursor, cpfs_funcionarios_disponiveis, num_registros):
    print(f"Populando EDUCADOR_FISICO com {num_registros} registros...")
    if not cpfs_funcionarios_disponiveis or num_registros == 0:
        print("  Aviso: Não há CPFs de funcionários ou num_registros é 0 para EDUCADOR_FISICO.")
        return []

    educadores_data = []
    # Garante que não selecionaremos mais CPFs do que os disponíveis e que não ultrapasse o limite desejado
    num_a_selecionar = min(num_registros, len(cpfs_funcionarios_disponiveis))
    cpfs_selecionados = random.sample(cpfs_funcionarios_disponiveis, num_a_selecionar)
    
    # Tenta garantir que educadores tenham formação em Ed. Física
    cpfs_ed_fisica = []
    outros_cpfs = []
    try:
        cursor.execute("SELECT CPF_INTERNO, FORMACAO FROM FUNCIONARIO WHERE CPF_INTERNO = ANY(%s)", (cpfs_selecionados,))
        resultados = cursor.fetchall()
        for cpf, formacao in resultados:
            if formacao == 'Educação Física':
                cpfs_ed_fisica.append(cpf)
            else:
                outros_cpfs.append(cpf)
    except Exception as e:
         print(f"  Erro ao buscar formação de funcionários: {e}")
         cpfs_ed_fisica = cpfs_selecionados # Usa todos se a busca falhar
         outros_cpfs = []

    # Prioriza quem tem formação, depois completa com outros se necessário
    cpfs_para_educador = cpfs_ed_fisica + outros_cpfs 
    cpfs_para_educador = cpfs_para_educador[:num_a_selecionar] # Garante o limite

    num_conselhos_gerados = set()
    for cpf in cpfs_para_educador:
        num_conselho = None
        while num_conselho is None or num_conselho in num_conselhos_gerados:
            num_conselho = f"CREF{fake.random_number(digits=6, fix_len=True)}/{fake.state_abbr()}"
        
        educadores_data.append((cpf, num_conselho))
        num_conselhos_gerados.add(num_conselho)

    sql = "INSERT INTO EDUCADOR_FISICO (CPF_FUNCIONARIO, NUMERO_CONSELHO) VALUES (%s, %s)"
    try:
        cursor.executemany(sql, educadores_data)
        print(f"  Inseridos {len(educadores_data)} registros em EDUCADOR_FISICO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em EDUCADOR_FISICO: {e}")
        return []
    return cpfs_para_educador # CPFs dos que se tornaram educadores

def popular_funcionario_atribuicao(cursor, cpfs_funcionarios):
    print("Populando FUNCIONARIO_ATRIBUICAO...")
    if not cpfs_funcionarios: return
    
    atribuicoes_data = []
    for cpf in cpfs_funcionarios:
        # Cada funcionário pode ter de 1 a 3 atribuições
        num_atribuicoes = random.randint(1, 3)
        atribuicoes_escolhidas = random.sample(ATRIBUICOES_FUNCIONARIO, num_atribuicoes)
        for atrib in atribuicoes_escolhidas:
            atribuicoes_data.append((cpf, atrib))
            
    sql = "INSERT INTO FUNCIONARIO_ATRIBUICAO (CPF_FUNCIONARIO, ATRIBUICAO) VALUES (%s, %s)"
    try:
        cursor.executemany(sql, atribuicoes_data)
        print(f"  Inseridos {len(atribuicoes_data)} registros em FUNCIONARIO_ATRIBUICAO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em FUNCIONARIO_ATRIBUICAO: {e}")

def popular_funcionario_restricao(cursor, cpfs_funcionarios):
    print("Populando FUNCIONARIO_RESTRICAO...")
    if not cpfs_funcionarios: return
    
    restricoes_data = []
    # Seleciona uma amostra de funcionários para ter restrições (ex: 20%)
    cpfs_com_restricao = random.sample(cpfs_funcionarios, k=len(cpfs_funcionarios) // 5) 
    
    for cpf in cpfs_com_restricao:
        # Cada funcionário com restrição pode ter 1 ou 2
        num_restricoes = random.randint(1, 2)
        restricoes_escolhidas = random.sample(RESTRICOES_FISICAS, num_restricoes)
        for restr in restricoes_escolhidas:
            restricoes_data.append((cpf, restr))
            
    sql = "INSERT INTO FUNCIONARIO_RESTRICAO (CPF_FUNCIONARIO, RESTRICAO_FISICA) VALUES (%s, %s)"
    try:
        cursor.executemany(sql, restricoes_data)
        print(f"  Inseridos {len(restricoes_data)} registros em FUNCIONARIO_RESTRICAO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em FUNCIONARIO_RESTRICAO: {e}")

def popular_instalacao(cursor, num_registros):
    print(f"Populando INSTALACAO com {num_registros} registros...")
    instalacoes_data = []
    ids_instalacoes = []

    instalacoes_unicas = []
    for tipo, nomes in NOMES_INSTALACOES_POR_TIPO.items():
        for nome in nomes:
            instalacoes_unicas.append((nome, tipo))
    
    # Garante que não tentamos selecionar mais instalações do que as únicas disponíveis
    if num_registros > len(instalacoes_unicas):
        print(f"  Aviso: Número de instalações ({num_registros}) é maior que o número de nomes únicos disponíveis ({len(instalacoes_unicas)}).")
        num_registros = len(instalacoes_unicas)

    # Seleciona 'num_registros' instalações únicas da lista
    instalacoes_selecionadas = random.sample(instalacoes_unicas, num_registros)

    for nome, tipo in instalacoes_selecionadas:
        capacidade = random.randint(10, 200) # Capacidade aleatória
        # Regra semântica: Vestiário não deve ser reservável
        eh_reservavel = 'Sim' if tipo != 'Vestiário' else 'Nao' 
        instalacoes_data.append((nome, tipo, capacidade, eh_reservavel))
    
    sql = """
        INSERT INTO INSTALACAO (NOME, TIPO, CAPACIDADE, EH_RESERVAVEL)
        VALUES (%s, %s, %s, %s)
        RETURNING ID_INSTALACAO
    """
    try:
        # Loop mantido para usar o RETURNING ID_INSTALACAO
        for data_tuple in instalacoes_data: 
            cursor.execute(sql, data_tuple)
            returned_id = cursor.fetchone()[0] 
            ids_instalacoes.append(returned_id)
        print(f"  Inseridos {len(instalacoes_data)} registros em INSTALACAO.")
    except Exception as e:
        cursor.connection.rollback()
        # Este erro ocorreria se (NOME, TIPO) duplicasse
        print(f"  Erro em INSTALACAO: {e}") 
        return []
    return ids_instalacoes

def popular_equipamento(cursor, num_registros, ids_instalacoes):
    print(f"Populando EQUIPAMENTO com {num_registros} registros...")
    if not ids_instalacoes:
        print("  Aviso: Não há IDs de instalações disponíveis para EQUIPAMENTO.")
        return []

    equipamentos_data = []
    patrimonios_gerados = set()
    for _ in range(num_registros):
        id_patrimonio = None
        while id_patrimonio is None or id_patrimonio in patrimonios_gerados:
            id_patrimonio = f"P{fake.unique.random_number(digits=7, fix_len=True)}"
        
        nome = random.choice(NOMES_EQUIPAMENTOS)
        id_instalacao = random.choice(ids_instalacoes)
        preco_aquisicao = round(Decimal(random.uniform(100.0, 5000.0)), 2)
        data_aquisicao = fake.date_between(start_date='-5y', end_date='today')

        equipamentos_data.append((id_patrimonio, nome, id_instalacao, preco_aquisicao, data_aquisicao))
        patrimonios_gerados.add(id_patrimonio)

    sql = """
        INSERT INTO EQUIPAMENTO (ID_PATRIMONIO, NOME, ID_INSTALACAO_LOCAL, PRECO_AQUISICAO, DATA_AQUISICAO)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(sql, equipamentos_data)
        print(f"  Inseridos {len(equipamentos_data)} registros em EQUIPAMENTO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em EQUIPAMENTO: {e}")
        return []
    return list(patrimonios_gerados)

def popular_doacao(cursor, num_registros, ids_equipamentos, cpfs_pessoas):
    print(f"Populando DOACAO com {num_registros} registros...")
    if not ids_equipamentos or not cpfs_pessoas:
        print("  Aviso: Não há IDs de equipamentos ou CPFs de pessoas disponíveis para DOACAO.")
        return

    doacoes_data = []
    equipamentos_disponiveis = ids_equipamentos.copy()
    num_a_selecionar = min(num_registros, len(equipamentos_disponiveis))
    equipamentos_selecionados = random.sample(equipamentos_disponiveis, num_a_selecionar)

    for id_equipamento in equipamentos_selecionados:
        cpf_doador = random.choice(cpfs_pessoas)
        data_doacao = fake.date_between(start_date='-2y', end_date='today')
        doacoes_data.append((id_equipamento, cpf_doador, data_doacao))

    sql = """
        INSERT INTO DOACAO (ID_EQUIPAMENTO, CPF_DOADOR, DATA_DOACAO)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.executemany(sql, doacoes_data)
        print(f"  Inseridos {len(doacoes_data)} registros em DOACAO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em DOACAO: {e}")

def popular_reserva(cursor, num_registros, ids_instalacoes, cpfs_internos):
    print(f"Populando RESERVA com {num_registros} registros...")
    if not ids_instalacoes or not cpfs_internos:
        print("  Aviso: Não há IDs de instalações ou CPFs de internos disponíveis para RESERVA.")
        return []

    reservas_data = []
    ids_reservas = []
    instalacoes_reservaveis = []
    
    # Filtra instalações que são reserváveis
    try:
        cursor.execute(f"SELECT ID_INSTALACAO FROM {SCHEMA}.INSTALACAO WHERE EH_RESERVAVEL = 'Sim'")
        resultados = cursor.fetchall()
        instalacoes_reservaveis = [row[0] for row in resultados]
    except Exception as e:
        print(f"  Erro ao buscar instalações reserváveis: {e}")
        return []

    if not instalacoes_reservaveis:
        print("  Aviso: Nenhuma instalação é reservável.")
        return []

    tripletos_unicos = set()
    
    max_tentativas = num_registros * 5 
    tentativas = 0
    
    while len(tripletos_unicos) < num_registros and tentativas < max_tentativas:
        id_instalacao = random.choice(instalacoes_reservaveis)
        cpf_interno = random.choice(cpfs_internos)
        data_reserva = fake.date_between(start_date='today', end_date='+30d')
        hora_inicio = time(hour=random.randint(6, 20), minute=0)
        
        triplete = (id_instalacao, data_reserva, hora_inicio)
        
        if triplete not in tripletos_unicos:
            tripletos_unicos.add(triplete)
            hora_fim = time(hour=hora_inicio.hour + random.randint(1, 3), minute=0)
            reservas_data.append((id_instalacao, cpf_interno, data_reserva, hora_inicio, hora_fim))
        
        tentativas += 1
    
    if tentativas >= max_tentativas:
        print(f"  Aviso: Atingido limite de tentativas. Gerando {len(reservas_data)}/{num_registros} reservas.")

    sql = """
        INSERT INTO RESERVA (ID_INSTALACAO, CPF_RESPONSAVEL_INTERNO, DATA_RESERVA, HORARIO_INICIO, HORARIO_FIM)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING ID_RESERVA
    """
    try:
        for data_tuple in reservas_data: 
            cursor.execute(sql, data_tuple)
            returned_id = cursor.fetchone()[0] 
            ids_reservas.append(returned_id)

        print(f"  Inseridos {len(reservas_data)} registros em RESERVA.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em RESERVA: {e}")
        return []
    return ids_reservas

def popular_atividade(cursor, num_registros):
    print(f"Populando ATIVIDADE com {num_registros} registros...")
    atividades_data = []
    ids_atividades = []
    
    # --- CORREÇÃO AQUI ---
    # Garante que o par (NOME, DATA_INICIO_PERIODO) seja único
    pares_unicos = set()
    
    # Limita o número de registros ao total de nomes de atividades disponíveis
    max_combinacoes = len(NOMES_ATIVIDADES)
    if num_registros > max_combinacoes:
         print(f"  Aviso: Reduzindo número de atividades para {max_combinacoes} (máximo de nomes únicos).")
         num_registros = max_combinacoes
         
    # Usa 'random.sample' para garantir nomes únicos, 
    # pois o nome é o principal fator de diferenciação.
    nomes_selecionados = random.sample(NOMES_ATIVIDADES, num_registros)
    
    for nome in nomes_selecionados:
        # Gera uma data de início. A chance de colisão (Nome + Data) 
        # agora é quase zero, pois os nomes são únicos.
        # Mas vamos manter a lógica do 'set' por segurança.
        
        data_inicio_periodo = fake.date_between(start_date='today')
        par = (nome, data_inicio_periodo)
        
        # Se por acaso (nome, data) colidir, tenta de novo
        while par in pares_unicos:
             data_inicio_periodo = fake.date_between(start_date='today')
             par = (nome, data_inicio_periodo)
             
        pares_unicos.add(par)
        
        vagas_limite = random.randint(5, 30)
        data_fim_periodo = data_inicio_periodo + timedelta(days=random.randint(30, 180))
        atividades_data.append((nome, vagas_limite, data_inicio_periodo, data_fim_periodo))

    sql = """
        INSERT INTO ATIVIDADE (NOME, VAGAS_LIMITE, DATA_INICIO_PERIODO, DATA_FIM_PERIODO)
        VALUES (%s, %s, %s, %s)
        RETURNING ID_ATIVIDADE
    """
    try:
        for data_tuple in atividades_data: 
            cursor.execute(sql, data_tuple)
            returned_id = cursor.fetchone()[0] 
            ids_atividades.append(returned_id)

        print(f"  Inseridos {len(atividades_data)} registros em ATIVIDADE.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em ATIVIDADE: {e}")
        return []
    return ids_atividades

def popular_ocorrencia_semanal(cursor, ids_atividades, ids_instalacoes, num_medio_ocorrencias):
    print("Populando OCORRENCIA_SEMANAL (com lógica semântica)...")
    if not ids_atividades or not ids_instalacoes:
        print("  Aviso: Não há IDs de atividades ou instalações disponíveis para OCORRENCIA_SEMANAL.")
        return

    # --- ETAPA 1: Buscar nomes das atividades ---
    atividades_map = {} # Dicionário: {id_atividade: 'Nome da Atividade'}
    try:
        cursor.execute(f"SELECT ID_ATIVIDADE, NOME FROM {SCHEMA}.ATIVIDADE WHERE ID_ATIVIDADE = ANY(%s)", (ids_atividades,))
        for row in cursor.fetchall():
            atividades_map[row[0]] = row[1]
    except Exception as e:
        print(f"  Erro ao buscar nomes das atividades: {e}")
        return # Não podemos continuar sem os nomes

    # --- ETAPA 2: Buscar e categorizar instalações por TIPO ---
    instalacoes_por_tipo = {} # Dicionário: {'Piscina': [101, 102], 'Quadra': [103, 104], ...}
    try:
        cursor.execute(f"SELECT ID_INSTALACAO, TIPO FROM {SCHEMA}.INSTALACAO WHERE ID_INSTALACAO = ANY(%s)", (ids_instalacoes,))
        for row in cursor.fetchall():
            id_inst, tipo = row[0], row[1]
            if tipo not in instalacoes_por_tipo:
                instalacoes_por_tipo[tipo] = []
            instalacoes_por_tipo[tipo].append(id_inst)
    except Exception as e:
        print(f"  Erro ao buscar tipos das instalações: {e}")
        return # Não podemos continuar sem os tipos

    # Lista de fallback: todas as instalações que NÃO são vestiários
    ids_instalacoes_gerais = []
    for tipo, ids in instalacoes_por_tipo.items():
        if tipo != 'Vestiário':
            ids_instalacoes_gerais.extend(ids)
    
    if not ids_instalacoes_gerais:
        print("  Aviso: Nenhuma instalação geral (não-vestiário) disponível.")
        ids_instalacoes_gerais = ids_instalacoes # Failsafe

    # --- ETAPA 3: Função de Mapeamento Semântico ---
    def get_lista_instalacoes_compativeis(nome_atividade):
        nome_lower = nome_atividade.lower()
        
        # Mapeia palavras-chave para tipos de instalação
        if 'natação' in nome_lower or 'hidroginástica' in nome_lower:
            return instalacoes_por_tipo.get('Piscina')
            
        if 'yoga' in nome_lower or 'ginástica' in nome_lower or 'dança' in nome_lower or \
           'alongamento' in nome_lower or 'ritmos' in nome_lower or 'karatê' in nome_lower or \
           'kung fu' in nome_lower or 'capoeira' in nome_lower or 'tai chi' in nome_lower:
            return instalacoes_por_tipo.get('Sala')
            
        if 'funcional' in nome_lower or 'muscular' in nome_lower or 'condicionamento' in nome_lower:
            return instalacoes_por_tipo.get('Academia')
            
        if 'futebol' in nome_lower:
            return instalacoes_por_tipo.get('Campo')
            
        if 'vôlei' in nome_lower or 'futsal' in nome_lower or 'basquete' in nome_lower or \
           'tênis' in nome_lower or 'peteca' in nome_lower or 'beach tennis' in nome_lower:
            return instalacoes_por_tipo.get('Quadra')

        # Se não houver mapeamento, retorna None (para usar a lista geral)
        return None

    # --- ETAPA 4: Geração dos dados ---
    ocorrencias_data = []
    for id_atividade in ids_atividades:
        num_ocorrencias = random.randint(1, num_medio_ocorrencias * 2)
        dias_escolhidos = random.sample(DIAS_SEMANA, k=min(num_ocorrencias, len(DIAS_SEMANA)))
        
        nome_atividade = atividades_map.get(id_atividade, "")
        
        # Define a lista de instalações válidas para esta atividade
        lista_instalacoes_validas = get_lista_instalacoes_compativeis(nome_atividade)
        
        # Se a atividade não foi mapeada ou se o tipo mapeado não tem instalações cadastradas,
        # usa a lista geral de instalações (excluindo vestiários).
        if not lista_instalacoes_validas:
            lista_instalacoes_validas = ids_instalacoes_gerais

        for dia in dias_escolhidos:
            # Escolhe uma instalação APENAS da lista válida
            id_instalacao = random.choice(lista_instalacoes_validas) 
            
            hora_inicio = time(hour=random.randint(6, 20), minute=0)
            hora_fim = time(hour=hora_inicio.hour + random.randint(1, 3), minute=0)
            ocorrencias_data.append((id_atividade, dia, id_instalacao, hora_inicio, hora_fim))

    # --- ETAPA 5: Inserção ---
    sql = """
        INSERT INTO OCORRENCIA_SEMANAL (ID_ATIVIDADE, DIA_SEMANA, ID_INSTALACAO, HORA_INICIO, HORA_FIM)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(sql, ocorrencias_data)
        print(f"  Inseridos {len(ocorrencias_data)} registros em OCORRENCIA_SEMANAL.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em OCORRENCIA_SEMANAL: {e}")

def popular_conduz_atividade(cursor, cpfs_educadores, ids_atividades):
    print("Populando CONDUZ_ATIVIDADE...")
    if not cpfs_educadores or not ids_atividades:
        print("  Aviso: Não há CPFs de educadores ou IDs de atividades disponíveis para CONDUZ_ATIVIDADE.")
        return

    conduz_data = []
    for id_atividade in ids_atividades:
        cpf_educador = random.choice(cpfs_educadores)
        conduz_data.append((cpf_educador, id_atividade))

    sql = "INSERT INTO CONDUZ_ATIVIDADE (CPF_EDUCADOR_FISICO, ID_ATIVIDADE) VALUES (%s, %s)"
    try:
        cursor.executemany(sql, conduz_data)
        print(f"  Inseridos {len(conduz_data)} registros em CONDUZ_ATIVIDADE.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em CONDUZ_ATIVIDADE: {e}")

def popular_participacao_atividade(cursor, num_registros, cpfs_pessoas, ids_atividades, cpfs_internos):
    print(f"Populando PARTICIPACAO_ATIVIDADE com {num_registros} registros...")
    if not cpfs_pessoas or not ids_atividades or not cpfs_internos:
        print("  Aviso: Não há CPFs de pessoas, IDs de atividades ou CPFs de internos disponíveis para PARTICIPACAO_ATIVIDADE.")
        return

    participacoes_data = []
    
    pares_unicos = set()
    
    max_combinacoes = len(cpfs_pessoas) * len(ids_atividades)
    if num_registros > max_combinacoes:
        print(f"  Aviso: Reduzindo número de participações para {max_combinacoes} (máximo de combinações únicas).")
        num_registros = max_combinacoes

    while len(pares_unicos) < num_registros:
        cpf_participante = random.choice(cpfs_pessoas)
        id_atividade = random.choice(ids_atividades)
        pares_unicos.add((cpf_participante, id_atividade))

    for par in pares_unicos:
        cpf_participante, id_atividade = par
        cpf_responsavel_interno = random.choice(cpfs_internos)
        data_inscricao = fake.date_between(start_date='-1y', end_date='today')
        participacoes_data.append((cpf_participante, id_atividade, cpf_responsavel_interno, data_inscricao))

    sql = """
        INSERT INTO PARTICIPACAO_ATIVIDADE (CPF_PARTICIPANTE, ID_ATIVIDADE, CPF_CONVIDANTE_INTERNO, DATA_INSCRICAO)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.executemany(sql, participacoes_data)
        print(f"  Inseridos {len(participacoes_data)} registros em PARTICIPACAO_ATIVIDADE.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em PARTICIPACAO_ATIVIDADE: {e}")

def popular_evento(cursor, num_registros, nomes_eventos, ids_reservas):
    print(f"Populando EVENTO com {num_registros} registros...")
    if not nomes_eventos or not ids_reservas:
        print("  Aviso: Não há nomes de eventos ou IDs de reservas disponíveis para EVENTO.")
        return []

    eventos_data = []
    ids_eventos = []
    
    # Garante nomes de eventos únicos (NOME é UNIQUE)
    num_a_selecionar = min(num_registros, len(nomes_eventos), len(ids_reservas))
    if num_a_selecionar < num_registros:
         print(f"  Aviso: Número de eventos limitado a {num_a_selecionar} (pelo min(nomes, reservas)).")
         
    nomes_selecionados = random.sample(nomes_eventos, num_a_selecionar)
    
    # Copia dos IDs de reserva para garantir que não usamos o mesmo ID de reserva
    # para mais de um evento.
    ids_reservas_disponiveis = ids_reservas.copy()

    for nome in nomes_selecionados:
        if not ids_reservas_disponiveis:
             break # Segurança
        
        descricao = f"Evento: {nome} organizado pelo CEFER."
        # Usa .pop() para garantir que uma reserva seja usada por UM evento
        id_reserva = ids_reservas_disponiveis.pop(random.randint(0, len(ids_reservas_disponiveis)-1)) 
        
        # Busca a data de realização da reserva correspondente
        data_realizacao = None
        try:
             cursor.execute(f"SELECT DATA_RESERVA FROM {SCHEMA}.RESERVA WHERE ID_RESERVA = %s", (id_reserva,))
             data_realizacao = cursor.fetchone()[0]
        except Exception as e:
             print(f"  Erro ao buscar data da reserva {id_reserva}: {e}")
             data_realizacao = fake.date_between(start_date='today', end_date='+60d') # Fallback
        
        eventos_data.append((nome, descricao, data_realizacao, id_reserva))

    sql = """
        INSERT INTO EVENTO (NOME, DESCRICAO, DATA_REALIZACAO, ID_RESERVA)
        VALUES (%s, %s, %s, %s)
        RETURNING ID_EVENTO
    """
    try:
        for data_tuple in eventos_data: 
            cursor.execute(sql, data_tuple)
            returned_id = cursor.fetchone()[0] 
            ids_eventos.append(returned_id)

        print(f"  Inseridos {len(eventos_data)} registros em EVENTO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em EVENTO: {e}")
        return []
    return ids_eventos

def popular_supervisao_evento(cursor, cpfs_funcionarios, ids_eventos):
    print("Populando SUPERVISAO_EVENTO...")
    if not cpfs_funcionarios or not ids_eventos:
        print("  Aviso: Não há CPFs de funcionários ou IDs de eventos disponíveis para SUPERVISAO_EVENTO.")
        return

    supervisao_data = []
    for id_evento in ids_eventos:
        cpf_funcionario = random.choice(cpfs_funcionarios)
        supervisao_data.append((cpf_funcionario, id_evento))

    sql = "INSERT INTO SUPERVISAO_EVENTO (CPF_FUNCIONARIO, ID_EVENTO) VALUES (%s, %s)"
    try:
        cursor.executemany(sql, supervisao_data)
        print(f"  Inseridos {len(supervisao_data)} registros em SUPERVISAO_EVENTO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em SUPERVISAO_EVENTO: {e}")

def popular_grupo_extensao(cursor, num_registros, nomes_grupos, cpfs_internos):
    print(f"Populando GRUPO_EXTENSAO com {num_registros} registros...")
    if not nomes_grupos or not cpfs_internos:
        print("  Aviso: Não há nomes de grupos ou CPFs de internos disponíveis para GRUPO_EXTENSAO.")
        return []

    grupos_data = []

    num_a_selecionar = min(num_registros, len(nomes_grupos))
    nomes_selecionados = random.sample(nomes_grupos, num_a_selecionar)

    for nome in nomes_selecionados:
        descricao = f"Grupo de extensão: {nome} promovido pelo CEFER."
        cpf_responsavel = random.choice(cpfs_internos)
        grupos_data.append((nome, descricao, cpf_responsavel))

    sql = """
        INSERT INTO GRUPO_EXTENSAO (NOME_GRUPO, DESCRICAO, CPF_RESPONSAVEL_INTERNO)
        VALUES (%s, %s, %s)
        RETURNING NOME_GRUPO
    """
    try:
        cursor.executemany(sql, grupos_data)
        print(f"  Inseridos {len(grupos_data)} registros em GRUPO_EXTENSAO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em GRUPO_EXTENSAO: {e}")
        return []
    return nomes_selecionados

def popular_atividade_grupo_extensao(cursor, ids_atividades, nomes_grupos):
    print("Populando ATIVIDADE_GRUPO_EXTENSAO...")
    if not ids_atividades or not nomes_grupos:
        print("  Aviso: Não há IDs de atividades ou nomes de grupos disponíveis para ATIVIDADE_GRUPO_EXTENSAO.")
        return

    atividade_grupo_data = []
    for id_atividade in ids_atividades:
        nome_grupo = random.choice(nomes_grupos)
        atividade_grupo_data.append((id_atividade, nome_grupo))

    sql = "INSERT INTO ATIVIDADE_GRUPO_EXTENSAO (ID_ATIVIDADE, NOME_GRUPO) VALUES (%s, %s)"
    try:
        cursor.executemany(sql, atividade_grupo_data)
        print(f"  Inseridos {len(atividade_grupo_data)} registros em ATIVIDADE_GRUPO_EXTENSAO.")
    except Exception as e:
        cursor.connection.rollback()
        print(f"  Erro em ATIVIDADE_GRUPO_EXTENSAO: {e}")

# --- Função Principal ---
def main():
    print("Iniciando script de população do banco de dados...")
    # Limpa o cache de valores únicos do Faker
    fake.unique.clear()

    # Tenta conectar ao banco de dados usando DBSession
    try:
        with DBSession(schema=SCHEMA) as db:
            with db.connection.cursor() as cursor:
                
                # 0. Limpar tabelas antes de popular (opcional, mas recomendado para testes)
                limpar_tabelas(cursor) 
                db.connection.commit() # Commit após limpeza

                # 1. Popular PESSOA
                lista_cpfs_pessoa = popular_pessoa(cursor, NUM_PESSOAS)
                db.connection.commit()

                # 2. Popular INTERNO_USP
                lista_cpfs_interno, internos_por_cat = popular_interno_usp(cursor, lista_cpfs_pessoa, NUM_INTERNOS_USP)
                db.connection.commit()
                
                # Garante que temos a lista correta de CPFs para funcionários
                cpfs_para_funcionario = internos_por_cat.get('FUNCIONARIO', [])

                # 3. Popular FUNCIONARIO
                lista_cpfs_funcionario = popular_funcionario(cursor, cpfs_para_funcionario)
                db.connection.commit()

                # 4. Popular EDUCADOR_FISICO (subset de FUNCIONARIO)
                lista_cpfs_educador = popular_educador_fisico(cursor, lista_cpfs_funcionario, NUM_EDUCADORES)
                db.connection.commit()

                # 5. Popular FUNCIONARIO_ATRIBUICAO e FUNCIONARIO_RESTRICAO
                popular_funcionario_atribuicao(cursor, lista_cpfs_funcionario)
                db.connection.commit()
                popular_funcionario_restricao(cursor, lista_cpfs_funcionario)
                db.connection.commit()
                
                # 6. Popular INSTALACAO
                lista_ids_instalacao = popular_instalacao(cursor, NUM_INSTALACOES)
                db.connection.commit()

                # 7. Popular EQUIPAMENTO
                lista_patrimonios = popular_equipamento(cursor, NUM_EQUIPAMENTOS, lista_ids_instalacao)
                db.connection.commit()

                # 8. Popular DOACAO
                if lista_patrimonios and lista_cpfs_pessoa:
                    popular_doacao(cursor, NUM_DOACOES, lista_patrimonios, lista_cpfs_pessoa)
                    db.connection.commit()
                
                # 9. Popular RESERVA
                lista_ids_reserva = popular_reserva(cursor, NUM_RESERVAS, lista_ids_instalacao, lista_cpfs_interno)
                db.connection.commit()

                # 10. Popular ATIVIDADE
                lista_ids_atividade = popular_atividade(cursor, NUM_ATIVIDADES)
                db.connection.commit()

                # 11. Popular OCORRENCIA_SEMANAL
                if lista_ids_atividade and lista_ids_instalacao:
                    popular_ocorrencia_semanal(cursor, lista_ids_atividade, lista_ids_instalacao, NUM_OCORRENCIAS_POR_ATIVIDADE)
                    db.connection.commit()

                # 12. Popular CONDUZ_ATIVIDADE
                if lista_cpfs_educador and lista_ids_atividade:
                    popular_conduz_atividade(cursor, lista_cpfs_educador, lista_ids_atividade)
                    db.connection.commit()
                
                # 13. Popular PARTICIPACAO_ATIVIDADE
                if lista_cpfs_pessoa and lista_ids_atividade and lista_cpfs_interno:
                    popular_participacao_atividade(cursor, NUM_PARTICIPACOES, lista_cpfs_pessoa, lista_ids_atividade, lista_cpfs_interno)
                    db.connection.commit()

                # 14. Popular EVENTO
                lista_ids_evento = popular_evento(cursor, NUM_EVENTOS, NOMES_EVENTOS, lista_ids_reserva)
                db.connection.commit()

                # 15. Popular SUPERVISAO_EVENTO
                if lista_cpfs_funcionario and lista_ids_evento:
                    popular_supervisao_evento(cursor, lista_cpfs_funcionario, lista_ids_evento)
                    db.connection.commit()
                
                # 16. Popular GRUPO_EXTENSAO
                lista_ids_grupo_extensao = popular_grupo_extensao(cursor, NUM_GRUPOS_EXTENSAO, NOMES_GRUPOS_EXTENSAO, lista_cpfs_interno)
                db.connection.commit()

                # 17. Popular ATIVIDADE_GRUPO_EXTENSAO
                if lista_ids_atividade and lista_ids_grupo_extensao:
                    popular_atividade_grupo_extensao(cursor, lista_ids_atividade, lista_ids_grupo_extensao)
                    db.connection.commit()

    except psycopg2.OperationalError as e:
        print(f"\nErro de conexão com o banco de dados: {e}")
        print("Verifique se o container Docker do PostgreSQL está rodando ('docker compose up -d')")
        print("e se as credenciais em dbsession.py estão corretas.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()