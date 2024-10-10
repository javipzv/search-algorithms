from utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SHIFT
import math
from graph.graph import Graph, Vertex
import regex as re

def cartesian_to_geo(x, y, min_lat, max_lat, min_lon, max_lon) -> tuple:
    """
    Transform Cartesian coordinates to geographic coordinates
    """
    lon = -(-min_lon + ((min_lon - max_lon) * x / SCREEN_WIDTH))
    lat = max_lat - ((max_lat - min_lat) * y / SCREEN_HEIGHT)
    return lat, lon

def geo_to_cartesian(lat, lon, min_lat, max_lat, min_lon, max_lon) -> tuple:
    """
    Transform geographic coordinates to Cartesian coordinates
    """
    x = (min_lon - lon) * (SCREEN_WIDTH) / (min_lon - max_lon)
    y = (max_lat - lat) * (SCREEN_HEIGHT) / (max_lat - min_lat)
    return SHIFT + x, y 

def euclidian_distance(lat1, lon1, lat2, lon2) -> float:
    """
    Calculate the Euclidean distance between two points
    """
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def get_nearest_node(graph, lat, lon) -> Vertex:
    """
    Get the nearest node to a given point selected by the user
    """
    vertices = graph.get_vertices()
    min_dist = float('inf')
    nearest_node = None
    
    for v in vertices:
        dist = euclidian_distance(lat, lon, v.latitude, v.longitude)
        if dist < min_dist:
            min_dist = dist
            nearest_node = v
    return nearest_node

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

def transform_final_path(city_limits: list, graph: Graph, path: list[Vertex]):
    """
    Transform the final path to geographic coordinates
    """
    transformed_path = []
    for i in range(len(path) - 1):
        edge = graph.get_edge_by_vertices(path[i], path[i + 1])
        if edge:
            line_coords = re.findall(r"(-?\d{1,2}\.\d*) (-?\d{1,2}\.\d*)", str(edge.linestring))
            coords_float = [(float(lat), float(lon)) for lon, lat in line_coords]
            transformed_path.extend(coords_float)

    transformed_path_to_cartesian = [geo_to_cartesian(lat, lon, min_lat=city_limits[0][0], max_lat=city_limits[0][1], 
                                                      min_lon=city_limits[1][0], max_lon=city_limits[1][1]) for lat, lon in transformed_path]
    return transformed_path_to_cartesian