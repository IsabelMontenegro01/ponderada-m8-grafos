import networkx as nx

from algoritmos import dijkstra, prim


# Criação do grafo da atividade.
grafo = nx.Graph()

grafo.add_nodes_from(["S0", "S1", "S2", "S3",
                      "S4", "S5", "S6", "S7"])

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
        raise ValueError("O peso da aresta não pode ser negativo.")

    grafo.add_edge(u, v, peso=peso)


# Exibição da matriz de adjacência.
print("MATRIZ DE ADJACÊNCIA")

vertices = list(grafo.nodes())

print("     " + "  ".join(vertices))

for u in vertices:
    linha = [u]

    for v in vertices:
        if grafo.has_edge(u, v):
            linha.append(str(grafo[u][v]["peso"]))
        else:
            linha.append("—")

    print("  ".join(f"{valor:>4}" for valor in linha))


# Dijkstra: caminho de S0 até S6.
print("\nDIJKSTRA")

origem = "S0"
destino = "S6"

distancias, antecessores, fechados, caminho, historico = dijkstra(
    grafo, origem, destino
)

# Exibição das iterações.
print("\nTabela de execução:")

for i, etapa in enumerate(historico, start=1):
    print(f"\nIteração {i} - vértice fechado: {etapa['vertice']}")

    print("Distâncias:")
    for v in vertices:
        distancia = etapa["distancias"][v]

        if distancia == float("inf"):
            print(f"{v}: ∞", end=" | ")
        else:
            print(f"{v}: {distancia}", end=" | ")

    print("\nAntecessores:")
    for v in vertices:
        print(f"{v}: {etapa['antecessores'][v]}", end=" | ")

    print()


print("\nOrdem de fechamento:")
print(" -> ".join(fechados))

print("\nAntecessores finais:")
for v in vertices:
    print(f"{v}: {antecessores[v]}")

print("\nMenor caminho:")
print(" -> ".join(caminho))

print(f"Custo mínimo: {distancias[destino]} km")


# Soma das distâncias mínimas a partir de S0.
soma_distancias = sum(distancias.values())

print(f"\nSoma das distâncias mínimas a partir de S0: "
      f"{soma_distancias} km")


# Contingência: falha do ramal e5 (S2-S4).
print("\nCONTINGÊNCIA - FALHA DO RAMAL e5")

grafo_contingencia = grafo.copy()
grafo_contingencia.remove_edge("S2", "S4")

distancias_novas, antecessores_novos, fechados_novos, caminho_novo, historico_novo = dijkstra(
    grafo_contingencia, origem, destino
)

novo_custo = distancias_novas[destino]
aumento = novo_custo - distancias[destino]
percentual = (aumento / distancias[destino]) * 100

print("Novo caminho:", " -> ".join(caminho_novo))
print(f"Novo custo: {novo_custo} km")
print(f"Aumento: {aumento} km")
print(f"Aumento percentual: {percentual:.2f}%")


# Árvore geradora mínima com Prim.
print("\nÁRVORE GERADORA MÍNIMA - PRIM")

arvore, custo_total = prim(grafo, origem)

for u, v, peso in arvore:
    print(f"{u} - {v}: {peso} km")

print(f"Custo total da AGM: {custo_total} km")

print("\nCOMPARAÇÃO")
print(f"Soma das distâncias de Dijkstra: {soma_distancias} km")
print(f"Custo da árvore geradora mínima: {custo_total} km")