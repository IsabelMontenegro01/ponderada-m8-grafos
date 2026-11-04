def dijkstra(grafo, origem, destino):
    vertices = list(grafo.nodes())

    distancias = {v: float("inf") for v in vertices}
    antecessores = {v: None for v in vertices}
    abertos = vertices.copy()
    fechados = []
    historico = []

    distancias[origem] = 0

    while abertos:
        # Seleciona o vértice aberto com menor distância.
        # Em caso de empate, considera o menor índice.
        u = min(
            abertos,
            key=lambda v: (distancias[v], vertices.index(v))
        )

        if distancias[u] == float("inf"):
            break

        abertos.remove(u)
        fechados.append(u)

        # Atualiza as distâncias dos vizinhos.
        for v in grafo.neighbors(u):
            if v in abertos:
                peso = grafo[u][v]["peso"]
                nova_distancia = distancias[u] + peso

                if nova_distancia < distancias[v]:
                    distancias[v] = nova_distancia
                    antecessores[v] = u

        # Guarda os valores após cada iteração.
        historico.append({
            "vertice": u,
            "distancias": distancias.copy(),
            "antecessores": antecessores.copy()
        })

        if u == destino:
            break

    # Reconstrói o caminho mínimo.
    caminho = []
    atual = destino

    if distancias[destino] != float("inf"):
        while atual is not None:
            caminho.append(atual)
            atual = antecessores[atual]

        caminho.reverse()

    return distancias, antecessores, fechados, caminho, historico


def prim(grafo, inicio):
    vertices = list(grafo.nodes())
    visitados = [inicio]
    arvore = []
    custo_total = 0

    while len(visitados) < len(vertices):
        menor_peso = float("inf")
        menor_aresta = None

        for u in vertices:
            if u in visitados:
                for v in grafo.neighbors(u):
                    if v not in visitados:
                        peso = grafo[u][v]["peso"]

                        if peso < menor_peso:
                            menor_peso = peso
                            menor_aresta = (u, v, peso)

        if menor_aresta is None:
            raise ValueError("O grafo não é conexo.")

        u, v, peso = menor_aresta

        arvore.append((u, v, peso))
        visitados.append(v)
        custo_total += peso

    return arvore, custo_total