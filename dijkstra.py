import numpy as np
import heapq
from math import inf
from graph import Graph

def dijkstra(g: Graph, source: str, destination: str):
    # Declare structures
    distances : dict = {v: inf for v in g.get_vertex()}
    seen : dict = {v: False for v in g.get_vertex()}
    vertices_queue : list = []

    # Update source's data
    distances[source] = 0
    seen[source] = True
    heapq.heappush(vertices_queue, (distances[source], source))

    # Iterate over the graph
    while vertices_queue:
        v : str = heapq.heappop(vertices_queue)
        v_distance : int = v[0]
        v_name : str = v[1]
        if v_name == destination:
            break
        seen[v_name] = True
        for neighbor, w in g.get_neighbors(v_name):
            if not seen[neighbor]:
                if v_distance + w < distances[neighbor]:
                    distances[neighbor] = v_distance + w
                    heapq.heappush(vertices_queue, (distances[neighbor], neighbor))

    # Return the final distance
    return distances[destination]

g = Graph()        

g.add_edge("uno", "tres", 2)
g.add_edge("uno", "cinco", 1)
g.add_edge("uno", "seis", 3)
g.add_edge("uno", "cuatro", 10)

g.add_edge("dos", "tres", 20)
g.add_edge("dos", "cuatro", 2)

g.add_edge("tres", "cinco", 4)
g.add_edge("tres", "seis", 3)

g.show_graph()

print()
print(dijkstra(g, "uno", "dos"))