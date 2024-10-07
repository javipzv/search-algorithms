import numpy as np
import heapq
from math import inf
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

def heuristic_function(v1: Vertex, v2: Vertex, distance_type: str = "Manhattan"):
    if distance_type == "Euclidean":
        return np.sqrt((v1.latitude - v2.latitude)**2 + (v1.longitude - v2.longitude)**2)
    elif distance_type == "Manhattan":
        return np.abs(v1.latitude - v2.latitude) + np.abs(v1.longitude - v2.longitude)
    else:
        raise Exception("Not valid heuristic")

def A_star(g: Graph, source: Vertex, destination: Vertex):
    # Declare structures
    distances: dict = {v: float(inf) for v in g.get_vertices()}
    seen: dict = {v: False for v in g.get_vertices()}
    parent_dict: dict = {v: None for v in g.get_vertices()}
    vertices_queue: list = []

    # Update source's data
    distances[source] = 0
    heapq.heappush(vertices_queue, (distances[source], source))

    # Iterate over the graph
    while vertices_queue:
        _, v = heapq.heappop(vertices_queue)

        # If we reached the destination
        if v == destination:
            break
        
        seen[v] = True
        for neighbor, w in g.get_neighbors(v):
            if not seen[neighbor]:
                new_distance: float = distances[v] + w
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent_dict[neighbor] = v
                    # Add the heuristic
                    priority = new_distance + heuristic_function(neighbor, destination)
                    heapq.heappush(vertices_queue, (priority, neighbor))
    
    # Return the solution
    if distances[destination] == float(inf):
        return "Not reached node"
    path = redo_path(destination, parent_dict)
    return distances[destination], path