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
        v_distance, v = heapq.heappop(vertices_queue)

        # If we reached the destination
        if v == destination:
            break
        
        seen[v] = True
        for neighbor, w in g.get_neighbors(v):
            if not seen[neighbor]:
                new_distance: float = v_distance + w
                if v_distance + w < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent_dict[neighbor] = v
                    heapq.heappush(vertices_queue, (distances[neighbor], neighbor))

    # Return the solution
    if distances[destination] == float(inf):
        return "Not reached node"
    path = redo_path(destination, parent_dict)
    return distances[destination], path

# g = Graph()        

# uno = Vertex("1", 0, 0)
# dos = Vertex("2", 0, 0)
# tres = Vertex("3", 0, 0)
# cuatro = Vertex("4", 0, 0)
# cinco = Vertex("5", 0, 0)
# seis = Vertex("6", 0, 0)

# g.add_edge(uno, tres, 2)
# g.add_edge(uno, cinco, 1)
# g.add_edge(uno, seis, 3)
# g.add_edge(dos, tres, 2)
# g.add_edge(dos, cuatro, 2)
# g.add_edge(tres, cinco, 4)
# g.add_edge(tres, seis, 3)
# g.add_edge(uno, cuatro, 5)

# g.show_graph()

# print()
# print(dijkstra(g, uno, cuatro))