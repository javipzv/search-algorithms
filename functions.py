from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SHIFT
import math
import pickle

def cartesian_to_geo(x, y, min_lat, max_lat, min_lon, max_lon):
    lon = -(-min_lon + ((min_lon - max_lon) * x / SCREEN_WIDTH))
    lat = max_lat - ((max_lat - min_lat) * y / SCREEN_HEIGHT)
    return lon, lat

def geo_to_cartesian(lon, lat, min_lat, max_lat, min_lon, max_lon):
    x = (min_lon - lon) * (SCREEN_WIDTH) / (min_lon - max_lon)
    y = (max_lat - lat) * (SCREEN_HEIGHT) / (max_lat - min_lat)
    return SHIFT + x, y 

def euclidian_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def get_nearest_node(graph, lon, lat):
    vertices = graph.get_vertices()
    min_dist = float('inf')
    nodo_cercano = None
    
    for v in vertices:
        dist = euclidian_distance(lat, lon, v.latitude, v.longitude)
        if dist < min_dist:
            min_dist = dist
            nodo_cercano = v
    return nodo_cercano

with open('maps/madrid_graph.pkl', 'rb') as archivo:
    madrid_graph = pickle.load(archivo)