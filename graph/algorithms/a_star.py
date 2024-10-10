import numpy as np
import heapq
from math import inf, radians, sin, cos, sqrt, atan2
from graph.graph import Graph, Vertex, Edge
import regex as re
from utils.helpers import redo_path

def redo_path(destination: Vertex, parent_map: dict):
    """
    Reconstruct the path from the destination to the source.
    """
    path = [destination]
    current_vertex = destination
    parent = parent_map[current_vertex]
    while parent:
        path.append(parent)
        current_vertex = parent
        parent = parent_map[current_vertex]
    return path[::-1]

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    """
    # Earth radius in kilometers
    R = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Difference between latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def heuristic_function(v1: Vertex, v2: Vertex, distance_type: str = "Euclidean", scale_factor: int = 1):
    """
    Heuristic function to estimate the distance between two vertices.
    """
    if distance_type == "Euclidean":
        return scale_factor * np.sqrt((v1.latitude - v2.latitude)**2 + (v1.longitude - v2.longitude)**2)
    elif distance_type == "Manhattan":
        return scale_factor * (np.abs(v1.latitude - v2.latitude) + np.abs(v1.longitude - v2.longitude))
    elif distance_type == "Haversine":
        return haversine_distance(v1.latitude, v1.longitude, v2.latitude, v2.longitude)
    else:
        raise Exception("Not valid heuristic")

def a_star(g: Graph, start_vertex: Vertex, end_vertex: Vertex):
    """
    A* algorithm to find the shortest path between two nodes.
    """

    # Declare structures
    shortest_distances: dict = {vertex: float(inf) for vertex in g.get_vertices()} # distances from the source to all nodes
    visited: set = set() # nodes already visited
    parent: dict = {vertex: None for vertex in g.get_vertices()} # stores parent of each node (to reconstruct the path)
    priority_queue: list = [] # priority queue for the vertices to be processed
    search_trace: list[Edge] = [] # store visited edges during the search

    # Initialize the start vertex
    shortest_distances[start_vertex] = 0
    heapq.heappush(priority_queue, (shortest_distances[start_vertex], start_vertex))

    # Main A* loop
    while priority_queue:
        _, current_vertex = heapq.heappop(priority_queue)

        # Update the trace of the path
        if parent[current_vertex]:
            parent_vertex = parent[current_vertex]
            edge = g.get_edge_by_vertices(parent_vertex, current_vertex)
            linestring = re.findall(r"(-?\d{1,2}\.\d*) (-?\d{1,2}\.\d*)", str(edge.linestring))
            linestring_floats = [(float(lon), float(lat)) for lon, lat in linestring]
            full_edge_path = [(parent_vertex.longitude, parent_vertex.latitude)] + linestring_floats + [(current_vertex.longitude, current_vertex.latitude)]
            search_trace.append(full_edge_path)

        # If we reached the destination
        if current_vertex == end_vertex:
            break
        
        visited.add(current_vertex)

        # Process neighbors of the current vertex
        for neighbor, edge_weight in g.get_neighbors(current_vertex):
            if neighbor not in visited:
                new_distance: float = shortest_distances[current_vertex] + edge_weight
                if new_distance < shortest_distances[neighbor]:
                    shortest_distances[neighbor] = new_distance
                    parent[neighbor] = current_vertex
                    
                    # Calculate the priority with the heuristic
                    priority: float = new_distance + heuristic_function(neighbor, end_vertex, distance_type="Euclidean", scale_factor=75000)
                    heapq.heappush(priority_queue, (priority, neighbor))
    
    # Return the solution: if destination is unreachable, return a message
    if shortest_distances[end_vertex] == float(inf):
        return "Node not reached"
    
    # Reconstruct the shortest path
    path = redo_path(end_vertex, parent)
    return shortest_distances[end_vertex], path, search_trace
