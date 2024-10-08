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

def dijkstra(g: Graph, source: Vertex, destination: Vertex):
    with open("trace.txt", "w") as file:
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
        v_distance, v = heapq.heappop(vertices_queue)

        # Data for painting
        if parent_dict[v]:
            v0 = parent_dict[v]
            edge = g.get_edge_by_vertices(v0, v)
            with open("trace.txt", "a") as file:
                file.write(str(v0.latitude) + " " + str(v0.longitude) + " " + str(v.latitude) + " " + str(v.longitude) + " " + str(edge.linestring) + "\n")

        # If we reached the destination
        if v == destination:
            break
        
        seen.add(v)
        for neighbor, w in g.get_neighbors(v):
            if neighbor not in seen:
                new_distance: float = v_distance + w
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent_dict[neighbor] = v
                    heapq.heappush(vertices_queue, (distances[neighbor], neighbor))

    # Return the solution
    if distances[destination] == float(inf):
        return "Not reached node"
    path = redo_path(destination, parent_dict)
    return distances[destination], len(path)