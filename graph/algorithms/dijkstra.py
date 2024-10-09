import numpy as np
import heapq
from math import inf
from graph.graph import Graph, Vertex
import regex as re

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
    # with open("traces/trace_dijkstra.txt", "w") as file:
    #     file.write("")
    trace = []

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
        # if parent_dict[v]:
        #     v0 = parent_dict[v]
        #     edge = g.get_edge_by_vertices(v0, v)
        #     with open("traces/trace_dijkstra.txt", "a") as file:
        #         file.write(str(v0.latitude) + " " + str(v0.longitude) + " " + str(v.latitude) + " " + str(v.longitude) + " " + str(edge.linestring) + "\n")
        if parent_dict[v]:
            v0 = parent_dict[v]
            edge = g.get_edge_by_vertices(v0, v)
            linestring = re.findall("(-?\d{1,2}\.\d*) (-?\d{1,2}\.\d*)", str(edge.linestring))
            linestring_float = [(float(a), float(b)) for a, b in linestring]
            p = [(v0.longitude, v0.latitude)] + linestring_float + [(v.longitude, v.latitude)]
            trace.append(p)

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
    return distances[destination], path, trace