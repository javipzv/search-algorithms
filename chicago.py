import osmnx as ox
import matplotlib.pyplot as plt
import time
from graph.graph import Graph, Vertex
from graph.algorithms.dijkstra import dijkstra
from graph.algorithms.a_star import a_star

# Create my own graph
my_g = Graph()

# Load Chicago graph
G = ox.load_graphml(filepath='graph_examples/chicago.graphml')

# Load the nodes and add them to my graph
nodes = G.nodes(data=True)
for node_id, attributes in nodes:
    v = Vertex(node_id, attributes['y'], attributes['x'])
    my_g.add_vertex(v)

# Load the edges and add them to my graph
edges = G.edges(data=True)
for u, v, attributes in edges:
    v1, v2 = my_g.get_vertex_by_id(u), my_g.get_vertex_by_id(v)
    my_g.add_edge(v1, v2, attributes['length'], attributes.get('geometry', ""))

# node_to_highlight = [list(G.nodes)[0], list(G.nodes)[12000]]  # Ejemplo: primeros dos nodos
# node_colors = ['red' if node in node_to_highlight else 'blue' for node in G.nodes()]
# node_sizes = [25 if node in node_to_highlight else 0.5 for node in G.nodes()]

# fig, ax = ox.plot_graph(G, node_size=node_sizes, node_color=node_colors, edge_color="white", edge_linewidth=0.1)
# plt.show()

source = my_g.vertices[list(G.nodes)[4000]]
destination = my_g.vertices[list(G.nodes)[18000]]

print(source, destination)
print()
a_star_start_time = time.perf_counter()

print(a_star(my_g, source, destination))

a_star_end_time = time.perf_counter()

print(f"TOTAL A_STAR TIME: {a_star_end_time - a_star_start_time}")
print()

dijkstra_start_time = time.perf_counter()

print(dijkstra(my_g, source, destination))

dijkstra_end_time = time.perf_counter()
print(f"TOTAL DIJKSTRA TIME: {dijkstra_end_time - dijkstra_start_time}")