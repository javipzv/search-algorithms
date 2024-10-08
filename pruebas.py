import osmnx as ox
import matplotlib.pyplot as plt
import time
from graph import Graph, Vertex
from dijkstra import dijkstra
from a_star import a_star

# Load Madrid OSM
G = ox.load_graphml(filepath='chicago.graphml')

# Inicializar las variables para almacenar los límites de latitud y longitud
min_lat = float('inf')
max_lat = float('-inf')
min_lon = float('inf')
max_lon = float('-inf')

# Cargar los nodos y añadirlos al grafo, al mismo tiempo que se calculan los extremos
nodes = G.nodes(data=True)
for node_id, attributes in nodes:
    lat = attributes['y']  # Latitud
    lon = attributes['x']  # Longitud
    
    # Actualizar los valores mínimos y máximos de latitud y longitud
    if lat < min_lat:
        min_lat = lat
    if lat > max_lat:
        max_lat = lat
    if lon < min_lon:
        min_lon = lon
    if lon > max_lon:
        max_lon = lon

# Imprimir los valores finales de las coordenadas mínimas y máximas
print(f"Mínima latitud: {min_lat}, Máxima latitud: {max_lat}")
print(f"Mínima longitud: {min_lon}, Máxima longitud: {max_lon}")