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

# g = Graph()        

# uno = Vertex("1", 0, 0)
# dos = Vertex("2", 0, 0)
# tres = Vertex("3", 0, 0)
# cuatro = Vertex("4", 0, 0)
# cinco = Vertex("5", 0, 0)
# seis = Vertex("6", 0, 0)

# g.add_edge(uno, tres, 2, 0)
# g.add_edge(uno, cinco, 1, 0)
# g.add_edge(uno, seis, 3, 0)
# g.add_edge(dos, tres, 2, 0)
# g.add_edge(dos, cuatro, 2, 0)
# g.add_edge(tres, cinco, 4, 0)
# g.add_edge(tres, seis, 3, 0)
# g.add_edge(uno, cuatro, 5, 0)

# g.show_graph()

# print()
# print(dijkstra(g, uno, dos))

# g = Graph()

# S = Vertex("S", 0, 0)
# A = Vertex("A", 0, 0)
# C = Vertex("C", 0, 0)
# E = Vertex("E", 0, 0)
# D = Vertex("D", 0, 0)
# B = Vertex("B", 0, 0)
# F = Vertex("F", 0, 0)
# T = Vertex("T", 0, 0)

# g.add_edge(S, A, 30, None)
# g.add_edge(A, C, 5, None)
# g.add_edge(A, E, 30, None)
# g.add_edge(A, B, 40, None)
# g.add_edge(C, D, 40, None)
# g.add_edge(E, F, 65, None)
# g.add_edge(D, B, 5, None)
# g.add_edge(D, T, 35, None)
# g.add_edge(B, T, 30, None)
# g.add_edge(F, T, 40, None)

# h_func = {"S": 90, "A": 65, "C": 70, "E": 100, "D": 25, "B": 20, "F": 20, "T": 0}

# print(dijkstra(g, S, T))