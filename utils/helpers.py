from utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SHIFT
import math
from graph.graph import Vertex

def cartesian_to_geo(x, y, min_lat, max_lat, min_lon, max_lon):
    """
    Transform Cartesian coordinates to geographic coordinates
    """
    lon = -(-min_lon + ((min_lon - max_lon) * x / SCREEN_WIDTH))
    lat = max_lat - ((max_lat - min_lat) * y / SCREEN_HEIGHT)
    return lon, lat

def geo_to_cartesian(lon, lat, min_lat, max_lat, min_lon, max_lon):
    """
    Transform geographic coordinates to Cartesian coordinates
    """
    x = (min_lon - lon) * (SCREEN_WIDTH) / (min_lon - max_lon)
    y = (max_lat - lat) * (SCREEN_HEIGHT) / (max_lat - min_lat)
    return SHIFT + x, y 

def euclidian_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Euclidean distance between two points
    """
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def get_nearest_node(graph, lon, lat):
    """
    Get the nearest node to a given point selected by the user
    """
    vertices = graph.get_vertices()
    min_dist = float('inf')
    nodo_cercano = None
    
    for v in vertices:
        dist = euclidian_distance(lat, lon, v.latitude, v.longitude)
        if dist < min_dist:
            min_dist = dist
            nodo_cercano = v
    return nodo_cercano

def redo_path(destination: Vertex, parent_dict: dict):
    """
    Redo the path from the destination to the source
    """
    path = [destination]
    child = destination
    parent = parent_dict[child]
    while parent:
        path.append(parent)
        child = parent
        parent = parent_dict[child]
    return path[::-1]