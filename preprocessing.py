import osmnx as ox
import pickle
import re
from graph.graph import Graph, Vertex
from utils.constants import MADRID_LIMITS, BARCELONA_LIMITS
from utils.helpers import geo_to_cartesian

def load_graph_edges_and_vertices(graph_filepath, lat_min_limit, lat_max_limit, lon_min_limit, lon_max_limit) -> tuple[list, Graph]:
    """
    Loads a graph from a file and extracts its edges and vertices within the given geographical limits.
    """
    # Create an empty graph
    custom_graph: Graph = Graph()
    
    # Load the graph using osmnx
    osmnx_graph = ox.load_graphml(filepath=graph_filepath)
    nodes: list = osmnx_graph.nodes(data=True)
    edges: list = osmnx_graph.edges(data=True)
    transformed_edges: list = []

    # Initialize the geographic bounds
    min_lat, max_lat = float('inf'), float('-inf')
    min_lon, max_lon = float('inf'), float('-inf')

    # Add vertices (nodes) within the geographic limits to the custom graph
    for node_id, attributes in nodes:
        lat, lon = attributes['y'], attributes['x']
        if lat_min_limit < lat < lat_max_limit and lon_min_limit < lon < lon_max_limit:
            vertex = Vertex(node_id, lat, lon)
            custom_graph.add_vertex(vertex)
            
            # Update geographic bounds
            min_lat = min(min_lat, lat)
            max_lat = max(max_lat, lat)
            min_lon = min(min_lon, lon)
            max_lon = max(max_lon, lon)

    # Add edges that connect vertices within the custom graph
    for u, v, attributes in edges:
        vertex_u: Vertex = custom_graph.get_vertex_by_id(u)
        vertex_v: Vertex = custom_graph.get_vertex_by_id(v)
        if vertex_u and vertex_v:
            edge_geometry = attributes.get('geometry', "")
            custom_graph.add_edge(vertex_u, vertex_v, attributes['length'], edge_geometry)
            
            # Process the edge's geometry if available
            edge_path = [(vertex_u.longitude, vertex_u.latitude)]
            if edge_geometry:
                line_coords = re.findall(r"(-?\d{1,2}\.\d*) (-?\d{1,2}\.\d*)", str(edge_geometry))
                coords_float = [(float(lon), float(lat)) for lon, lat in line_coords]
                edge_path.extend(coords_float)
            
            edge_path.append((vertex_v.longitude, vertex_v.latitude))
            
            # Convert geographic coordinates to Cartesian
            transformed_edge = [geo_to_cartesian(lon, lat, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon) for lon, lat in edge_path]
            transformed_edges.append(transformed_edge)

    return transformed_edges, custom_graph

# Process Madrid graph
madrid_edges, madrid_graph = load_graph_edges_and_vertices(
    graph_filepath='graph/graph_examples/madrid.graphml',
    lat_min_limit=MADRID_LIMITS[1][0], lat_max_limit=MADRID_LIMITS[1][1], 
    lon_min_limit=MADRID_LIMITS[0][0], lon_max_limit=MADRID_LIMITS[0][1]
)

# Process Barcelona graph
barcelona_edges, barcelona_graph = load_graph_edges_and_vertices(
    graph_filepath='graph/graph_examples/barcelona.graphml',
    lat_min_limit=BARCELONA_LIMITS[1][0], lat_max_limit=BARCELONA_LIMITS[1][1], 
    lon_min_limit=BARCELONA_LIMITS[0][0], lon_max_limit=BARCELONA_LIMITS[0][1]
)

# Save the results for Madrid
with open('graphs_data/madrid_edges.pkl', 'wb') as file:
    pickle.dump(madrid_edges, file)

with open('graphs_data/madrid_graph.pkl', 'wb') as file:
    pickle.dump(madrid_graph, file)

# Save the results for Barcelona
with open('graphs_data/barcelona_edges.pkl', 'wb') as file:
    pickle.dump(barcelona_edges, file)

with open('graphs_data/barcelona_graph.pkl', 'wb') as file:
    pickle.dump(barcelona_graph, file)