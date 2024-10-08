import osmnx as ox
import matplotlib.pyplot as plt
import time
from graph.graph import Graph, Vertex
from graph.algorithms.dijkstra import dijkstra
from graph.algorithms.a_star import a_star

# Create my own graph
my_g = Graph()

# Load Madrid OSM
G = ox.load_graphml(filepath='graph_examples/grafo_madrid.graphml')

# Load the nodes and add them to my graph
nodes = G.nodes(data=True)
for node_id, attributes in nodes:
    if attributes['y'] > 40.36 and attributes['y'] < 40.47 and attributes['x'] > -3.77 and attributes['x'] < -3.62:
        v = Vertex(node_id, attributes['y'], attributes['x'])
        my_g.add_vertex(v)

print(my_g.get_number_of_vertex())
# Load the edges and add them to my graph
edges = G.edges(data=True)
for u, v, attributes in edges:
    if my_g.get_vertex_by_id(u) and my_g.get_vertex_by_id(v):
        v1, v2 = my_g.get_vertex_by_id(u), my_g.get_vertex_by_id(v)
        my_g.add_edge(v1, v2, attributes['length'], attributes.get('geometry', ""))

# node_to_highlight = [list(G.nodes)[30000], list(G.nodes)[17000]]  # Ejemplo: primeros dos nodos
# node_colors = ['red' if node in node_to_highlight else 'blue' for node in G.nodes()]
# node_sizes = [25 if node in node_to_highlight else 0.5 for node in G.nodes()]

# # Crea la figura y los ejes
# fig, ax = ox.plot_graph(G, node_size=node_sizes, node_color=node_colors, edge_color="white", edge_linewidth=0.1)


# fig, ax = ox.plot_graph(G, node_size=0.2, edge_color="blue", edge_linewidth=0.2)
# plt.show()

# my_g.show_graph()

source = my_g.vertices[list(G.nodes)[7000]]
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