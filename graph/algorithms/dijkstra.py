import heapq
from math import inf
from graph.graph import Graph, Vertex, Edge
import regex as re
from utils.helpers import redo_path

def dijkstra(g: Graph, start_vertex: Vertex, end_vertex: Vertex):
    """
    Dijkstra algorithm to find the shortest path between two nodes.
    """

    # Declare structures
    shortest_distances: dict = {vertex: float(inf) for vertex in g.get_vertices()}  # distances from the source to all nodes
    visited: set = set()  # nodes already visited
    parent: dict = {vertex: None for vertex in g.get_vertices()}  # stores parent of each node (to reconstruct the path)
    priority_queue: list = []  # priority queue for the vertices to be processed
    search_trace: list[Edge] = []  # store visited edges during the search

    # Initialize the start vertex's distance and push it into the priority queue
    shortest_distances[start_vertex] = 0
    heapq.heappush(priority_queue, (shortest_distances[start_vertex], start_vertex))

    # Main Dijkstra loop
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Update the trace of the path by adding the current edge
        if parent[current_vertex]:
            parent_vertex = parent[current_vertex]
            edge = g.get_edge_by_vertices(parent_vertex, current_vertex)
            edge_path = re.findall(r"(-?\d{1,2}\.\d*) (-?\d{1,2}\.\d*)", str(edge.linestring))
            edge_path_floats = [(float(lon), float(lat)) for lon, lat in edge_path]
            full_edge_path = [(parent_vertex.longitude, parent_vertex.latitude)] + edge_path_floats + [(current_vertex.longitude, current_vertex.latitude)]
            search_trace.append(full_edge_path)

        # If we reached the destination, stop the search
        if current_vertex == end_vertex:
            break
        
        visited.add(current_vertex)

        # Process neighbors of the current vertex
        for neighbor, edge_weight in g.get_neighbors(current_vertex):
            if neighbor not in visited:
                new_distance: float = current_distance + edge_weight
                if new_distance < shortest_distances[neighbor]:
                    shortest_distances[neighbor] = new_distance
                    parent[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (shortest_distances[neighbor], neighbor))

    # Return the result: if destination is unreachable, return a message
    if shortest_distances[end_vertex] == float(inf):
        return "Node not reached"
    
    # Reconstruct the shortest path
    path = redo_path(end_vertex, parent)
    return shortest_distances[end_vertex], path, search_trace
