import networkx as nx


def dijkstra(grafo, origem, destino):
    vertices = list(grafo.nodes())

    distancias = {v: float("inf") for v in vertices}
    antecessores = {v: None for v in vertices}
    fechados = []
    abertos = vertices.copy()

    distancias[origem] = 0

    while abertos:
        # Escolhe o vértice aberto com menor distância.
        # Em caso de empate, mantém o de menor índice.
        u = min(
            abertos,
            key=lambda v: (distancias[v], vertices.index(v))
        )

        if distancias[u] == float("inf"):
            break

        abertos.remove(u)
        fechados.append(u)

        if u == destino:
            break

        # Atualiza as distâncias dos vizinhos ainda abertos.
        for v in grafo.neighbors(u):
            if v in abertos:
                peso = grafo[u][v]["peso"]
                nova_distancia = distancias[u] + peso

                if nova_distancia < distancias[v]:
                    distancias[v] = nova_distancia
                    antecessores[v] = u

    # Reconstrói o caminho a partir dos antecessores.
    caminho = []
    atual = destino

    if distancias[destino] != float("inf"):
        while atual is not None:
            caminho.append(atual)
            atual = antecessores[atual]

        caminho.reverse()

    return distancias, antecessores, fechados, caminho


def prim(grafo, inicio):
    vertices = list(grafo.nodes())
    visitados = {inicio}
    arestas_arvore = []
    custo_total = 0

    while len(visitados) < len(vertices):
        menor_aresta = None
        menor_peso = float("inf")

        # Procura a menor aresta que liga um vértice visitado
        # a outro que ainda não pertence à árvore.
        for u in visitados:
            for v in grafo.neighbors(u):
                if v not in visitados:
                    peso = grafo[u][v]["peso"]

                    if peso < menor_peso:
                        menor_peso = peso
                        menor_aresta = (u, v, peso)

        if menor_aresta is None:
            raise ValueError("O grafo não é conexo.")

        u, v, peso = menor_aresta

        arestas_arvore.append((u, v, peso))
        custo_total += peso
        visitados.add(v)

    return arestas_arvore, custo_total