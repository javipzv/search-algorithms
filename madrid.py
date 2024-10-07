import osmnx as ox
import matplotlib.pyplot as plt
import time
from graph import Graph, Vertex
from dijkstra import dijkstra
from a_star import A_star

# Create my own graph
my_g = Graph()

# Load Madrid OSM
G = ox.load_graphml(filepath='grafo_madrid.graphml')

# Load the nodes and add them to my graph
nodes = G.nodes(data=True)
for node_id, attributes in nodes:
    v = Vertex(node_id, attributes['y'], attributes['x'])
    my_g.add_vertex(v)

# Load the edges and add them to my graph
edges = G.edges(data=True)
for u, v, attributes in edges:
    v1, v2 = my_g.vertices[u], my_g.vertices[v]
    my_g.add_edge(v1, v2, attributes['length'])

node_to_highlight = [list(G.nodes)[30000], list(G.nodes)[17000]]  # Ejemplo: primeros dos nodos
node_colors = ['red' if node in node_to_highlight else 'blue' for node in G.nodes()]
node_sizes = [25 if node in node_to_highlight else 1 for node in G.nodes()]

# Crea la figura y los ejes
fig, ax = ox.plot_graph(G, node_size=node_sizes, node_color=node_colors, edge_color="blue", edge_linewidth=0.2)


# fig, ax = ox.plot_graph(G, node_size=0.2, edge_color="blue", edge_linewidth=0.2)
# plt.show()

# my_g.show_graph()

source = my_g.vertices[list(G.nodes)[30000]]
destination = my_g.vertices[list(G.nodes)[17000]]

print(source, destination)
print()
start_time = time.perf_counter()

print(dijkstra(my_g, source, destination))

end_time = time.perf_counter()

print()
print(f"TOTAL DIJKSTRA TIME: {end_time - start_time}")
print()
start_time = time.perf_counter()

print(A_star(my_g, source, destination))

end_time = time.perf_counter()

print()
print(f"TOTAL A_STAR TIME: {end_time - start_time}")