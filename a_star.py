import numpy as np
import heapq
from math import inf, radians, sin, cos, sqrt, atan2
from graph import Graph, Vertex

def redo_path(destination: Vertex, parent_dict: dict):
    # Recreate the shortest path iterating over the parents
    path = [destination]
    child = destination
    parent = parent_dict[child]
    while parent:
        path.append(parent)
        child = parent
        parent = parent_dict[child]
    return path[::-1]

def haversine_distance(lat1, lon1, lat2, lon2):
    # Earth radius
    R = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Diferencia entre las latitudes y longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def heuristic_function(v1: Vertex, v2: Vertex, distance_type: str = "Euclidean", scale_factor: int = 1):
    if distance_type == "Euclidean":
        return scale_factor * np.sqrt((v1.latitude - v2.latitude)**2 + (v1.longitude - v2.longitude)**2)
    elif distance_type == "Manhattan":
        return scale_factor * np.abs(v1.latitude - v2.latitude) + np.abs(v1.longitude - v2.longitude)
    elif distance_type == "Haversine":
        return haversine_distance(v1.latitude, v1.longitude, v2.latitude, v2.longitude)
    else:
        raise Exception("Not valid heuristic")

def a_star(g: Graph, source: Vertex, destination: Vertex):
    
    with open("trace_astar.txt", "w") as file:
        file.write("")

    # Declare structures
    distances: dict = {v: float(inf) for v in g.get_vertices()}
    seen: set = set()
    parent_dict: dict = {v: None for v in g.get_vertices()}
    vertices_queue: list = []

    # Update source's data
    distances[source] = 0
    heapq.heappush(vertices_queue, (distances[source], source))

    # Iterate over the graph
    while vertices_queue:
        _, v = heapq.heappop(vertices_queue)

        # Data for painting
        if parent_dict[v]:
            v0 = parent_dict[v]
            edge = g.get_edge_by_vertices(v0, v)
            with open("trace_astar.txt", "a") as file:
                file.write(str(v0.latitude) + " " + str(v0.longitude) + " " + str(v.latitude) + " " + str(v.longitude) + " " + str(edge.linestring) + "\n")

        # If we reached the destination
        if v == destination:
            break
        
        seen.add(v)
        for neighbor, w in g.get_neighbors(v):
            if neighbor not in seen:
                new_distance: float = distances[v] + w
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent_dict[neighbor] = v
                    # Add the heuristic
                    priority: float = new_distance + heuristic_function(neighbor, destination, distance_type="Euclidean", scale_factor=75000)
                    heapq.heappush(vertices_queue, (priority, neighbor))
    
    # Return the solution
    if distances[destination] == float(inf):
        return "Not reached node"
    path = redo_path(destination, parent_dict)
    return distances[destination], len(path)