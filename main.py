
import networkx as nx

from algoritmos import dijkstra, prim


def criar_grafo():
    grafo = nx.Graph()

    # Oito subestações.
    grafo.add_nodes_from([f"S{i}" for i in range(8)])

    # Treze ramais e seus respectivos pesos.
    arestas = [
        ("S0", "S1", 12),
        ("S0", "S2", 17),
        ("S1", "S2", 9),
        ("S1", "S3", 12),
        ("S2", "S4", 15),
        ("S2", "S5", 14),
        ("S3", "S4", 8),
        ("S3", "S6", 15),
        ("S4", "S5", 7),
        ("S4", "S7", 17),
        ("S5", "S7", 24),
        ("S6", "S7", 13),
        ("S1", "S4", 23)
    ]

    for u, v, peso in arestas:
        if peso < 0:
            raise ValueError("O peso de uma aresta não pode ser negativo.")

        grafo.add_edge(u, v, peso=peso)

    return grafo


def exibir_matriz(grafo):
    vertices = list(grafo.nodes())

    print("\nMATRIZ DE ADJACÊNCIA")
    print("     " + "  ".join(vertices))

    for u in vertices:
        linha = [u]

        for v in vertices:
            if grafo.has_edge(u, v):
                valor = grafo[u][v]["peso"]
                linha.append(str(valor))
            else:
                linha.append("—")

        print("  ".join(f"{valor:>4}" for valor in linha))


def executar_dijkstra(grafo):
    origem = "S0"
    destino = "S6"

    distancias, antecessores, fechados, caminho = dijkstra(
        grafo, origem, destino
    )

    print("\nDIJKSTRA")
    print(f"Origem: {origem}")
    print(f"Destino: {destino}")

    print("\nDistâncias finais:")
    for vertice, distancia in distancias.items():
        if distancia == float("inf"):
            print(f"{vertice}: Infinito")
        else:
            print(f"{vertice}: {distancia} km")

    print("\nAntecessores:")
    for vertice, antecessor in antecessores.items():
        print(f"{vertice}: {antecessor}")

    print("\nOrdem de fechamento:")
    print(" -> ".join(fechados))

    print("\nMenor caminho:")
    print(" -> ".join(caminho))

    print(f"Custo total: {distancias[destino]} km")

    return distancias, caminho


def executar_contingencia(grafo, custo_original):
    print("\nCONTINGÊNCIA: FALHA DO RAMAL e5 (S2-S4)")

    grafo_contingencia = grafo.copy()
    grafo_contingencia.remove_edge("S2", "S4")

    distancias, antecessores, fechados, caminho = dijkstra(
        grafo_contingencia, "S0", "S6"
    )

    novo_custo = distancias["S6"]
    aumento = novo_custo - custo_original
    percentual = (aumento / custo_original) * 100

    print("Novo caminho:", " -> ".join(caminho))
    print(f"Novo custo: {novo_custo} km")
    print(f"Aumento: {aumento} km")
    print(f"Aumento percentual: {percentual:.2f}%")


def executar_prim(grafo):
    arestas, custo_total = prim(grafo, "S0")

    print("\nÁRVORE GERADORA MÍNIMA (PRIM)")

    for u, v, peso in arestas:
        print(f"{u} - {v}: {peso} km")

    print(f"Custo total da AGM: {custo_total} km")


def main():
    grafo = criar_grafo()

    exibir_matriz(grafo)

    distancias, caminho = executar_dijkstra(grafo)

    executar_contingencia(grafo, distancias["S6"])

    executar_prim(grafo)


if __name__ == "__main__":
    main()