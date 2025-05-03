import heapq
import time
import random
import tracemalloc
from collections import defaultdict

__author__ = "Equipe A3 Estrutura de Dados (Depois colocar o numero do grupo)"
__version__ = "1.0.0"
__license__ = "MIT"

# 1. Função para gerar dados de teste completos
def gerar_dados(num_entregas, num_caminhoes):
    """
    Gera dados aleatórios para simulação de entregas e caminhões.
    
    Args:
        num_entregas: Número de entregas a serem geradas
        num_caminhoes: Número de caminhões disponíveis
        
    Returns:
        Tuple: (lista de entregas, lista de caminhões)
    """
    # Gerar entregas com destino, prazo e carga
    entregas = [{
        'id': i,
        'destino': f'Destino {i}', 
        'prazo': random.randint(24, 72),
        'carga': random.randint(50, 200)  # Carga entre 50-200 unidades
    } for i in range(num_entregas)]
    
    # Gerar caminhões com capacidade, horas limite e velocidade
    caminhoes = [{
        'id': i,
        'capacidade': random.randint(1000, 2000), 
        'horas_limite': random.randint(8, 12),
        'velocidade': random.randint(60, 80)  # Velocidade média em km/h
    } for i in range(num_caminhoes)]
    
    return entregas, caminhoes

# 2. Função para gerar o grafo de distâncias
def gerar_grafo_distancias_Grande(centros, destinos):
    """
    Cria um grafo de distâncias entre centros de distribuição e destinos.
    
    Args:
        centros: Lista de centros de distribuição
        destinos: Lista de destinos de entrega
        
    Returns:
        Dict: Grafo representado como dicionário de dicionários
    """
    grafo = {}
    
    # Distâncias dos centros para os destinos
    for centro in centros:
        grafo[centro] = {}
        for destino in destinos:
            # Distância aleatória entre 100 e 1000 km
            grafo[centro][destino] = random.randint(100, 1000)
    
    # Distâncias dos destinos para os centros (simétricas)
    for destino in destinos:
        grafo[destino] = {}
        for centro in centros:
            grafo[destino][centro] = grafo[centro][destino]
    
    return grafo

def gerar_grafo_distancias_Pequeno(centros, destinos):
    """
    Cria um grafo de distâncias entre centros de distribuição e destinos.
    
    Args:
        centros: Lista de centros de distribuição
        destinos: Lista de destinos de entrega
        
    Returns:
        Dict: Grafo representado como dicionário de dicionários
    """
    grafo = {}
    
    # Distâncias dos centros para os destinos
    for centro in centros:
        grafo[centro] = {}
        for destino in destinos:
            # Distância aleatória entre 30 e 200 km
            grafo[centro][destino] = random.randint(30, 200)
    
    # Distâncias dos destinos para os centros (simétricas)
    for destino in destinos:
        grafo[destino] = {}
        for centro in centros:
            grafo[destino][centro] = grafo[centro][destino]
    
    return grafo



# 3. Função para gerar matriz de adjacência
def gerar_matriz_adjacencia(nos, distancias):
    """
    Converte o grafo de distâncias em uma matriz de adjacência.
    
    Args:
        nos: Lista de todos os nós (centros + destinos)
        distancias: Grafo de distâncias como dicionário
        
    Returns:
        List: Matriz de adjacência n x n
    """
    n = len(nos)
    # Inicializa matriz com infinito em todas as posições
    matriz = [[float('inf')] * n for _ in range(n)]
    
    # Distância de um nó para ele mesmo é 0
    for i in range(n):
        matriz[i][i] = 0
    
    # Preenche as distâncias conhecidas
    for origem, destinos in distancias.items():
        i = nos.index(origem)
        for destino, distancia in destinos.items():
            j = nos.index(destino)
            matriz[i][j] = distancia
    
    return matriz

# 4. Funções para encontrar centro mais próximo
def centro_mais_proximo_lista(destino, grafo):
    """
    Encontra o centro de distribuição mais próximo usando lista de adjacência.
    
    Args:
        destino: Destino para encontrar centro mais próximo
        grafo: Grafo de distâncias como lista de adjacência
        
    Returns:
        Str: Nome do centro mais próximo
    """
    menor_distancia = float('inf')
    centro_mais_proximo = None
    
    for centro, distancias in grafo.items():
        # Ignorar nós que são destinos
        if centro.startswith('Destino'):
            continue
        if destino in distancias and distancias[destino] < menor_distancia:
            menor_distancia = distancias[destino]
            centro_mais_proximo = centro
    
    return centro_mais_proximo

def centro_mais_proximo_matriz(destino, matriz, nos):
    """
    Encontra o centro de distribuição mais próximo usando matriz de adjacência.
    
    Args:
        destino: Destino para encontrar centro mais próximo
        matriz: Matriz de adjacência
        nos: Lista de todos os nós
        
    Returns:
        Str: Nome do centro mais próximo
    """
    destino_idx = nos.index(destino)
    menor_distancia = float('inf')
    centro_mais_proximo = None
    
    for i, centro in enumerate(nos):
        # Ignorar nós que são destinos
        if centro.startswith('Destino'):
            continue
        if matriz[i][destino_idx] < menor_distancia:
            menor_distancia = matriz[i][destino_idx]
            centro_mais_proximo = centro
    
    return centro_mais_proximo

# 5. Implementações do algoritmo de Dijkstra
def dijkstra_lista(grafo, inicio, fim):
    """
    Implementação do Dijkstra usando lista simples.
    
    Args:
        grafo: Grafo como lista de adjacência
        inicio: Nó de início
        fim: Nó de destino
        
    Returns:
        Float: Menor distância entre inicio e fim
    """
    distancias = {no: float('inf') for no in grafo}
    distancias[inicio] = 0
    visitados = set()
    
    while True:
        no_atual = None
        menor_distancia = float('inf')
        
        # Encontra o nó não visitado mais próximo
        for no in grafo:
            if no not in visitados and distancias[no] < menor_distancia:
                no_atual = no
                menor_distancia = distancias[no]
        
        # Condições de parada
        if no_atual is None or no_atual == fim:
            break
        
        visitados.add(no_atual)
        
        # Atualiza distâncias dos vizinhos
        for vizinho, distancia_vizinho in grafo[no_atual].items():
            nova_distancia = distancias[no_atual] + distancia_vizinho
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
    
    return distancias[fim]

def dijkstra_heap(grafo, inicio, fim):
    """
    Implementação do Dijkstra usando heap para melhor desempenho.
    
    Args:
        grafo: Grafo como lista de adjacência
        inicio: Nó de início
        fim: Nó de destino
        
    Returns:
        Float: Menor distância entre inicio e fim
    """
    fila = []
    heapq.heappush(fila, (0, inicio))
    distancias = {no: float('inf') for no in grafo}
    distancias[inicio] = 0
    
    while fila:
        distancia, no_atual = heapq.heappop(fila)
        
        # Chegamos ao destino
        if no_atual == fim:
            return distancia
        
        # Já encontramos um caminho melhor
        if distancia > distancias[no_atual]:
            continue
        
        # Processa vizinhos
        for vizinho, distancia_vizinho in grafo[no_atual].items():
            nova_distancia = distancia + distancia_vizinho
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                heapq.heappush(fila, (nova_distancia, vizinho))
    
    return float('inf')

def dijkstra_matriz(matriz, inicio_idx, fim_idx):
    """
    Implementação do Dijkstra usando matriz de adjacência.
    
    Args:
        matriz: Matriz de adjacência
        inicio_idx: Índice do nó de início
        fim_idx: Índice do nó de destino
        
    Returns:
        Float: Menor distância entre inicio e fim
    """
    n = len(matriz)
    distancias = [float('inf')] * n
    distancias[inicio_idx] = 0
    visitados = [False] * n
    
    for _ in range(n):
        no_atual = -1
        menor_distancia = float('inf')
        
        # Encontra o nó não visitado mais próximo
        for i in range(n):
            if not visitados[i] and distancias[i] < menor_distancia:
                no_atual = i
                menor_distancia = distancias[i]
        
        # Condições de parada
        if no_atual == -1 or no_atual == fim_idx:
            break
        
        visitados[no_atual] = True
        
        # Atualiza distâncias dos vizinhos
        for vizinho in range(n):
            if (not visitados[vizinho] and 
                matriz[no_atual][vizinho] != float('inf')):
                nova_distancia = distancias[no_atual] + matriz[no_atual][vizinho]
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
    
    return distancias[fim_idx]

# 6. Funções auxiliares para alocação
def calcular_tempo_viagem(distancia_km, velocidade_kmh):
    """
    Calcula o tempo de viagem em horas.
    
    Args:
        distancia_km: Distância em quilômetros
        velocidade_kmh: Velocidade média em km/h
        
    Returns:
        Float: Tempo de viagem em horas
    """
    return distancia_km / velocidade_kmh

def alocar_entregas_centro(entregas, caminhoes, centro, grafo, nos=None):
    """
    Aloca entregas para caminhões em um centro específico.
    
    Args:
        entregas: Lista de entregas para o centro
        caminhoes: Lista de caminhões disponíveis
        centro: Centro de distribuição atual
        grafo: Grafo de distâncias
        nos: Lista de nós (para matriz de adjacência)
        
    Returns:
        Tuple: (lista de alocações, lista de caminhões restantes)
    """
    alocacoes = []
    caminhoes_restantes = caminhoes.copy()
    
    # Ordenar entregas por prazo (mais urgentes primeiro)
    entregas.sort(key=lambda x: x['prazo'])
    
    for caminhao in caminhoes:
        capacidade_restante = caminhao['capacidade']
        horas_disponiveis = caminhao['horas_limite']
        entregas_alocadas = []
        distancia_total = 0
        
        for entrega in [e for e in entregas if e not in entregas_alocadas]:
            # Calcular distância do centro para o destino
            if nos:  # Usar matriz de adjacência
                centro_idx = nos.index(centro)
                destino_idx = nos.index(entrega['destino'])
                distancia = dijkstra_matriz(grafo, centro_idx, destino_idx)
            else:    # Usar lista de adjacência
                distancia = dijkstra_heap(grafo, centro, entrega['destino'])
            
            tempo_viagem = calcular_tempo_viagem(distancia, caminhao['velocidade'])
            
            # Verificar se o caminhão pode atender a entrega
            if (entrega['carga'] <= capacidade_restante and 
                tempo_viagem <= horas_disponiveis):
                
                entregas_alocadas.append(entrega)
                capacidade_restante -= entrega['carga']
                horas_disponiveis -= tempo_viagem
                distancia_total += distancia
        
        if entregas_alocadas:
            alocacoes.append({
                'caminhao': caminhao,
                'centro': centro,
                'entregas': entregas_alocadas,
                'distancia_total': distancia_total,
                'tempo_total': distancia_total / caminhao['velocidade']
            })
            # Remover caminhão alocado
            caminhoes_restantes.remove(caminhao)
            # Remover entregas alocadas
            entregas = [e for e in entregas if e not in entregas_alocadas]
    
    return alocacoes, caminhoes_restantes

# 7. Função principal de alocação otimizada
def alocar_caminhoes_otimizado(entregas, caminhoes, grafo, nos=None):
    """
    Algoritmo principal de alocação de caminhões considerando todas as restrições.
    
    Args:
        entregas: Lista de todas as entregas
        caminhoes: Lista de todos os caminhões
        grafo: Grafo de distâncias
        nos: Lista de nós (para matriz de adjacência)
        
    Returns:
        List: Lista de alocações completas
    """
    # 1. Agrupar entregas por centro de distribuição mais próximo
    entregas_por_centro = defaultdict(list)
    
    for entrega in entregas:
        destino = entrega['destino']
        if nos:  # Usar matriz de adjacência
            centro = centro_mais_proximo_matriz(destino, grafo, nos)
        else:    # Usar lista de adjacência
            centro = centro_mais_proximo_lista(destino, grafo)
        entregas_por_centro[centro].append(entrega)
    
    # 2. Alocar caminhões para cada centro
    alocacoes_totais = []
    caminhoes_disponiveis = caminhoes.copy()
    
    for centro, entregas_centro in entregas_por_centro.items():
        alocacoes, caminhoes_disponiveis = alocar_entregas_centro(
            entregas_centro, caminhoes_disponiveis, centro, grafo, nos)
        alocacoes_totais.extend(alocacoes)
    
    return alocacoes_totais

# 8. Funções para exibição de resultados
def exibir_alocacoes(alocacoes):
    """
    Exibe as alocações de forma organizada e legível.
    
    Args:
        alocacoes: Lista de alocações geradas
    """
    print("\n=== RESUMO DE ALOCAÇÕES ===")
    print(f"Total de caminhões alocados: {len(alocacoes)}")
    
    for alocacao in alocacoes:
        print(f"\nCaminhão {alocacao['caminhao']['id']} (Capacidade: {alocacao['caminhao']['capacidade']}):")
        print(f"  - Centro de partida: {alocacao['centro']}")
        print(f"  - Distância total: {alocacao['distancia_total']:.2f} km")
        print(f"  - Tempo estimado: {alocacao['tempo_total']:.2f} horas (Limite: {alocacao['caminhao']['horas_limite']}h)")
        print(f"  - Carga utilizada: {sum(e['carga'] for e in alocacao['entregas'])}/{alocacao['caminhao']['capacidade']}")
        print("  - Entregas:")
        for entrega in alocacao['entregas']:
            print(f"    * {entrega['destino']} (Carga: {entrega['carga']}, Prazo: {entrega['prazo']}h)")

def medir_desempenho(entregas, caminhoes, grafo, algoritmo_dijkstra, nome_algoritmo, nos=None):
    """
    Mede o desempenho do algoritmo de roteamento.
    
    Args:
        entregas: Lista de entregas
        caminhoes: Lista de caminhões
        grafo: Grafo de distâncias
        algoritmo_dijkstra: Função do algoritmo a ser testado
        nome_algoritmo: Nome descritivo do algoritmo
        nos: Lista de nós (para matriz de adjacência)
    """
    tracemalloc.start()
    inicio_tempo = time.time()
    
    # Executar a alocação
    alocacoes = alocar_caminhoes_otimizado(entregas, caminhoes, grafo, nos)
    
    fim_tempo = time.time()
    memoria_usada = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    
    tempo_execucao = fim_tempo - inicio_tempo
    entregas_alocadas = sum(len(a['entregas']) for a in alocacoes)
    
    print(f"\n{algoritmo_dijkstra.__name__} - {nome_algoritmo}")
    print(f"  - Tempo de execução: {tempo_execucao:.6f} segundos")
    print(f"  - Consumo de memória: {memoria_usada} bytes")
    print(f"  - Entregas alocadas: {entregas_alocadas}/{len(entregas)}")
    print(f"  - Caminhões utilizados: {len(alocacoes)}/{len(caminhoes)}")

    
    
def Testepequeno():

    print(f"\n===================")
    print(f"===Teste Pequeno===")
    print(f"===================")
    
    # Configuração inicial
    random.seed(42)  # Para resultados reproduzíveis
    centros_distribuicao = ['Belém', 'Recife', 'Brasília', 'São Paulo', 'Florianópolis']
    
    # Gerar dados de teste
    num_entregas = 10 #ALTERA AQUI PRA MUDAR O TAMANHO DO TESTE DEFAULT 30
    num_caminhoes = 2 # DEFAULT 10
    entregas, caminhoes = gerar_dados(num_entregas, num_caminhoes)
    destinos = [entrega['destino'] for entrega in entregas]
    
    print(f"\n=== CONFIGURAÇÃO INICIAL ===")
    print(f"Centros de distribuição: {', '.join(centros_distribuicao)}")
    print(f"Total de entregas: {num_entregas}")
    print(f"Total de caminhões: {num_caminhoes}")
    
    # Gerar estruturas de dados
    grafo_distancias = gerar_grafo_distancias_Pequeno(centros_distribuicao, destinos)
    nos = centros_distribuicao + destinos
    matriz_adjacencia = gerar_matriz_adjacencia(nos, grafo_distancias)
    
    # Testar com lista de adjacência
    print("\n=== TESTE COM LISTA DE ADJACÊNCIA ===")
    alocacoes_lista = alocar_caminhoes_otimizado(entregas, caminhoes, grafo_distancias)
    exibir_alocacoes(alocacoes_lista)
    medir_desempenho(entregas, caminhoes, grafo_distancias, dijkstra_heap, "Lista de Adjacência")
    
    # Testar com matriz de adjacência
    print("\n=== TESTE COM MATRIZ DE ADJACÊNCIA ===")
    alocacoes_matriz = alocar_caminhoes_otimizado(entregas, caminhoes, matriz_adjacencia, nos)
    exibir_alocacoes(alocacoes_matriz)
    medir_desempenho(entregas, caminhoes, matriz_adjacencia, dijkstra_matriz, "Matriz de Adjacência", nos)
    
    # Comparação de desempenho entre algoritmos Dijkstra
    print("\n=== COMPARAÇÃO DE ALGORITMOS DIJKSTRA ===")
    medir_desempenho(entregas, caminhoes, grafo_distancias, dijkstra_lista, "Lista Simples")
    medir_desempenho(entregas, caminhoes, grafo_distancias, dijkstra_heap, "Heap")
    medir_desempenho(entregas, caminhoes, matriz_adjacencia, dijkstra_matriz, "Matriz", nos)
    

def TesteGrande():
    print(f"\n==================")
    print(f"===Teste Grande===")
    print(f"==================")
        
    # Configuração inicial
    random.seed(42)  # Para resultados reproduzíveis
    centros_distribuicao = ['Belém', 'Recife', 'Brasília', 'São Paulo', 'Florianópolis']
    
    # Gerar dados de teste
    num_entregas = 30 #ALTERA AQUI PRA MUDAR O TAMANHO DO TESTE DEFAULT 30
    num_caminhoes = 10 # DEFAULT 10
    entregas, caminhoes = gerar_dados(num_entregas, num_caminhoes)
    destinos = [entrega['destino'] for entrega in entregas]
    
    print(f"\n=== CONFIGURAÇÃO INICIAL ===")
    print(f"Centros de distribuição: {', '.join(centros_distribuicao)}")
    print(f"Total de entregas: {num_entregas}")
    print(f"Total de caminhões: {num_caminhoes}")
    
    # Gerar estruturas de dados
    grafo_distancias = gerar_grafo_distancias_Grande(centros_distribuicao, destinos)
    nos = centros_distribuicao + destinos
    matriz_adjacencia = gerar_matriz_adjacencia(nos, grafo_distancias)
    
    # Testar com lista de adjacência
    print("\n=== TESTE COM LISTA DE ADJACÊNCIA ===")
    alocacoes_lista = alocar_caminhoes_otimizado(entregas, caminhoes, grafo_distancias)
    exibir_alocacoes(alocacoes_lista)
    medir_desempenho(entregas, caminhoes, grafo_distancias, dijkstra_heap, "Lista de Adjacência")
    
    # Testar com matriz de adjacência
    print("\n=== TESTE COM MATRIZ DE ADJACÊNCIA ===")
    alocacoes_matriz = alocar_caminhoes_otimizado(entregas, caminhoes, matriz_adjacencia, nos)
    exibir_alocacoes(alocacoes_matriz)
    medir_desempenho(entregas, caminhoes, matriz_adjacencia, dijkstra_matriz, "Matriz de Adjacência", nos)
    
    # Comparação de desempenho entre algoritmos Dijkstra
    print("\n=== COMPARAÇÃO DE ALGORITMOS DIJKSTRA ===")
    medir_desempenho(entregas, caminhoes, grafo_distancias, dijkstra_lista, "Lista Simples")
    medir_desempenho(entregas, caminhoes, grafo_distancias, dijkstra_heap, "Heap")
    medir_desempenho(entregas, caminhoes, matriz_adjacencia, dijkstra_matriz, "Matriz", nos)
    
    
    
# 9. Função principal para execução do programa

Testepequeno();

TesteGrande();