import osmnx as ox
import matplotlib.pyplot as plt

# Descarga el grafo de las calles de Madrid
G = ox.load_graphml(filepath='grafo_madrid.graphml')

# nodes = G.nodes(data=True)
# for node_id, attributes in nodes:
#     print(f"Nodo {node_id}: {attributes}")

# edges = G.edges(data=True)
# for u, v, attributes in edges:
#     print(f"Arista desde nodo {u} hasta nodo {v}: {attributes}")

fig, ax = ox.plot_graph(G, node_size=0.2, edge_color="blue", edge_linewidth=0.2)
plt.show()