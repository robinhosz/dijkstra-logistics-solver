import heapq
import time
import sys
import random
import tracemalloc

# Função para gerar dados de teste
def gerar_dados(num_entregas, num_caminhoes):
    entregas = [{'destino': f'Destino {i}', 'prazo': random.randint(24, 72)} for i in range(num_entregas)]
    caminhoes = [{'capacidade': random.randint(1000, 2000), 'horas_limite': random.randint(8, 12)} for _ in range(num_caminhoes)]
    return entregas, caminhoes

# Função para gerar o grafo de distâncias dinamicamente
def gerar_grafo_distancias(centros, destinos):
    grafo = {}
    for centro in centros:
        grafo[centro] = {}
        for destino in destinos:
            grafo[centro][destino] = random.randint(100, 1000)  # Distância aleatória entre 100 e 1000 km
    for destino in destinos:
        grafo[destino] = {}
        for centro in centros:
            grafo[destino][centro] = grafo[centro][destino]  # Distância simétrica
    return grafo

# Função para gerar grafo como matriz de adjacência
def gerar_matriz_adjacencia(nos, distancias):
    n = len(nos)
    matriz = [[float('inf')] * n for _ in range(n)]  # Inicializa com infinito
    for i in range(n):
        matriz[i][i] = 0  # Distância de um nó para ele mesmo é 0
    for origem, destinos in distancias.items():
        i = nos.index(origem)
        for destino, distancia in destinos.items():
            j = nos.index(destino)
            matriz[i][j] = distancia
    return matriz

# Função para encontrar o centro de distribuição mais próximo (para lista de adjacência)
def centro_mais_proximo_lista(destino, grafo):
    menor_distancia = float('inf')
    centro_mais_proximo = None
    for centro, distancias in grafo.items():
        if centro.startswith('Destino'):  # Ignorar destinos
            continue
        if destino in distancias and distancias[destino] < menor_distancia:
            menor_distancia = distancias[destino]
            centro_mais_proximo = centro
    return centro_mais_proximo

# Função para encontrar o centro de distribuição mais próximo (para matriz de adjacência)
def centro_mais_proximo_matriz(destino, matriz, nos):
    destino_idx = nos.index(destino)
    menor_distancia = float('inf')
    centro_mais_proximo = None
    for i, centro in enumerate(nos):
        if centro.startswith('Destino'):  # Ignorar destinos
            continue
        if matriz[i][destino_idx] < menor_distancia:
            menor_distancia = matriz[i][destino_idx]
            centro_mais_proximo = centro
    return centro_mais_proximo

# Algoritmo de Dijkstra usando lista simples
def dijkstra_lista(grafo, inicio, fim):
    distancias = {no: float('inf') for no in grafo}
    distancias[inicio] = 0
    visitados = set()

    while True:
        no_atual = None
        menor_distancia = float('inf')
        for no in grafo:
            if no not in visitados and distancias[no] < menor_distancia:
                no_atual = no
                menor_distancia = distancias[no]
        if no_atual is None or no_atual == fim:
            break
        visitados.add(no_atual)
        for vizinho, distancia_vizinho in grafo[no_atual].items():
            if distancias[no_atual] + distancia_vizinho < distancias[vizinho]:
                distancias[vizinho] = distancias[no_atual] + distancia_vizinho
    return distancias[fim]

# Algoritmo de Dijkstra usando heap
def dijkstra_heap(grafo, inicio, fim):
    fila = []
    heapq.heappush(fila, (0, inicio))
    distancias = {no: float('inf') for no in grafo}
    distancias[inicio] = 0

    while fila:
        (distancia, no_atual) = heapq.heappop(fila)
        if no_atual == fim:
            return distancia
        if distancia > distancias[no_atual]:
            continue
        for vizinho, distancia_vizinho in grafo[no_atual].items():
            nova_distancia = distancia + distancia_vizinho
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                heapq.heappush(fila, (nova_distancia, vizinho))
    return float('inf')

# Algoritmo de Dijkstra usando matriz de adjacência
def dijkstra_matriz(matriz, inicio_idx, fim_idx):
    n = len(matriz)
    distancias = [float('inf')] * n
    distancias[inicio_idx] = 0
    visitados = [False] * n

    for _ in range(n):
        no_atual = -1
        menor_distancia = float('inf')
        for i in range(n):
            if not visitados[i] and distancias[i] < menor_distancia:
                no_atual = i
                menor_distancia = distancias[i]
        if no_atual == -1 or no_atual == fim_idx:
            break
        visitados[no_atual] = True
        for vizinho in range(n):
            if not visitados[vizinho] and matriz[no_atual][vizinho] != float('inf'):
                nova_distancia = distancias[no_atual] + matriz[no_atual][vizinho]
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
    return distancias[fim_idx]

# Função para alocar caminhões e calcular rotas
def alocar_caminhoes(entregas, caminhoes, grafo, algoritmo_dijkstra, nos=None):
    for entrega in entregas:
        destino = entrega['destino']
        if nos:  # Para matriz de adjacência
            centro = centro_mais_proximo_matriz(destino, grafo, nos)
            inicio_idx = nos.index(centro)
            fim_idx = nos.index(destino)
            distancia = algoritmo_dijkstra(grafo, inicio_idx, fim_idx)
        else:  # Para lista de adjacência
            centro = centro_mais_proximo_lista(destino, grafo)
            distancia = algoritmo_dijkstra(grafo, centro, destino)
        print(f"Entrega para {destino} será feita a partir de {centro} com distância {distancia} km")

# Medição de desempenho
def medir_desempenho(entregas, caminhoes, grafo, algoritmo_dijkstra, nome_algoritmo, nos=None):
    tracemalloc.start()  # Iniciar o rastreamento de memória
    inicio_tempo = time.time()
    alocar_caminhoes(entregas, caminhoes, grafo, algoritmo_dijkstra, nos)
    fim_tempo = time.time()
    memoria_usada = tracemalloc.get_traced_memory()[1]  # Memória usada em bytes
    tracemalloc.stop()  # Parar o rastreamento de memória
    tempo_execucao = fim_tempo - inicio_tempo
    print(f"{nome_algoritmo} - Tempo de execução: {tempo_execucao:.6f} segundos, Consumo de memória: {memoria_usada} bytes")

# Testes
centros_distribuicao = ['Belém', 'Recife', 'Brasília', 'São Paulo', 'Florianópolis']
entregas, caminhoes = gerar_dados(10, 5)  # 10 entregas, 5 caminhões
destinos = [entrega['destino'] for entrega in entregas]
grafo_distancias = gerar_grafo_distancias(centros_distribuicao, destinos)

# Lista de nós para matriz de adjacência
nos = centros_distribuicao + destinos
matriz_adjacencia = gerar_matriz_adjacencia(nos, grafo_distancias)
lista_adjacencia = grafo_distancias  # Já está no formato de lista de adjacência

# Teste com Dijkstra usando lista simples
print("Teste com Dijkstra (Lista Simples):")
medir_desempenho(entregas, caminhoes, lista_adjacencia, dijkstra_lista, "Dijkstra Lista Simples")

# Teste com Dijkstra usando heap
print("\nTeste com Dijkstra (Heap):")
medir_desempenho(entregas, caminhoes, lista_adjacencia, dijkstra_heap, "Dijkstra Heap")

# Teste com Dijkstra usando matriz de adjacência
print("\nTeste com Dijkstra (Matriz de Adjacência):")
medir_desempenho(entregas, caminhoes, matriz_adjacencia, dijkstra_matriz, "Dijkstra Matriz de Adjacência", nos)

# Teste com Dijkstra usando lista de adjacência
print("\nTeste com Dijkstra (Lista de Adjacência):")
medir_desempenho(entregas, caminhoes, lista_adjacencia, dijkstra_heap, "Dijkstra Lista de Adjacência")