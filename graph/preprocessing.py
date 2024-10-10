import osmnx as ox
import pickle
import re
from graph.graph import Graph, Vertex
from utils.constants import MADRID_LIMITS, CHICAGO_LIMITS, SCREEN_HEIGHT, SCREEN_WIDTH, SHIFT
from utils.helpers import geo_to_cartesian

def get_edges(graph_path, min_limit_lat, max_limit_lat, min_limin_lon, max_limit_lon):
    my_G = Graph()
    
    G = ox.load_graphml(filepath=graph_path)
    nodes = G.nodes(data=True)
    edges = G.edges(data=True)
    transformed_edges = []

    min_lat = float('inf')
    max_lat = float('-inf')
    min_lon = float('inf')
    max_lon = float('-inf')
    for node_id, attributes in nodes:
        if attributes['y'] > min_limit_lat and attributes['y'] < max_limit_lat and attributes['x'] > min_limin_lon and attributes['x'] < max_limit_lon:
            lat, lon = attributes['y'], attributes['x']
            v = Vertex(node_id, lat, lon)
            my_G.add_vertex(v)
            
            # Update
            if lat < min_lat:
                min_lat = lat
            if lat > max_lat:
                max_lat = lat
            if lon < min_lon:
                min_lon = lon
            if lon > max_lon:
                max_lon = lon

    for u, v, attributes in edges:
        if my_G.get_vertex_by_id(u) and my_G.get_vertex_by_id(v):
            pts = []
            v1, v2 = my_G.get_vertex_by_id(u), my_G.get_vertex_by_id(v)
            my_G.add_edge(v1, v2, attributes['length'], attributes.get('geometry', ""))
            pts.append((v1.longitude, v1.latitude))

            linestring = attributes.get('geometry', '')
            if linestring:
                coords_linestring = re.findall("(-?\d{1,2}\.\d*) (-?\d{1,2}\.\d*)", str(linestring))
                coords_linestring_to_float = [(float(a), float(b)) for a, b in coords_linestring]
                pts = pts + coords_linestring_to_float

            pts.append((v2.longitude, v2.latitude))
            pts_resized = [geo_to_cartesian(lon=lon, lat=lat, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon) for lon, lat in pts]
            transformed_edges.append(pts_resized)

    return transformed_edges, my_G

madrid_edges, madrid_graph = get_edges(graph_path='graph_examples/madrid.graphml', 
                         min_limit_lat=MADRID_LIMITS[1][0], max_limit_lat=MADRID_LIMITS[1][1], 
                         min_limin_lon=MADRID_LIMITS[0][0], max_limit_lon=MADRID_LIMITS[0][1])

chicago_edges, chicago_graph = get_edges(graph_path='graph_examples/chicago.graphml', 
                          min_limit_lat=CHICAGO_LIMITS[1][0], max_limit_lat=CHICAGO_LIMITS[1][1], 
                          min_limin_lon=CHICAGO_LIMITS[0][0], max_limit_lon=CHICAGO_LIMITS[0][1])

with open('maps/madrid_edges.pkl', 'wb') as file:
    pickle.dump(madrid_edges, file)

with open('maps/chicago_edges.pkl', 'wb') as file:
    pickle.dump(chicago_edges, file)

with open('maps/madrid_graph.pkl', 'wb') as file:
    pickle.dump(madrid_graph, file)

with open('maps/chicago_graph.pkl', 'wb') as file:
    pickle.dump(chicago_graph, file)