class Vertex:
    def __init__(self, id: str, latitude: float, longitude: float) -> None:
        self.id: str = id
        self.latitude: float = latitude
        self.longitude: float = longitude

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vertex):
            return self.id == other.id
        return False
    
    def __lt__(self, other: 'Vertex') -> bool:
        return self.id < other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Vertex (id={self.id}, lat={self.latitude}, lon={self.longitude})"

class Edge:
    def __init__(self, source_id, destination_id, weight, linestring) -> None:
        self.source_id = source_id
        self.destination_id = destination_id
        self.weight = weight
        self.linestring = linestring
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Edge):
            return self.source_id == other.source_id and self.destination_id == other.destination_id or \
                    self.source_id == self.destination_id and self.destination_id == other.source_id
        return False

    def __lt__(self, other: 'Vertex') -> bool:
        return self.source_id + self.destination_id < other.source_id + other.destination_id

    def __hash__(self) -> int:
        return hash((self.source_id, self.destination_id))

    def __repr__(self) -> str:
        return f"Edge (source_id={self.source_id}, destination_id={self.destination_id}, weight={self.weight})"

class Graph:
    def __init__(self, dirigido: bool = False):
        self.graph: dict = {}
        self.vertices: dict = {}
        self.edges: dict = {}
        self.dirigido: bool = dirigido

    def add_vertex(self, v: Vertex):
        self.graph[v] = []
        self.vertices[v.id] = v

    def add_edge(self, v1: Vertex, v2: Vertex, weight: int, linestring):
        if v1 not in self.graph:
            self.graph[v1] = []
            self.vertices[v1.id] = v1
        if v2 not in self.graph:
            self.graph[v2] = []
            self.vertices[v2.id] = v2
        self.graph[v1].append((v2, weight))
        self.edges[(min(v1.id, v2.id), max(v1.id, v2.id))] = Edge(v1.id, v2.id, weight, linestring)
        if not self.dirigido:
            self.graph[v2].append((v1, weight))

    def get_edge_by_vertices(self, v1: Vertex, v2: Vertex):
        return self.edges[(min(v1.id, v2.id), max(v1.id, v2.id))]

    def get_vertices(self):
        return [vertex for vertex, _ in self.graph.items()]

    def get_vertex_by_id(self, id):
        return self.vertices[id]

    def get_neighbors(self, v1: Vertex) -> list:
        return self.graph[v1]
    
    def get_number_of_vertex(self) -> int:
        return len(self.graph)
    
    def show_graph(self):
        for v, neighbors in self.graph.items():
            print(f"{v}: {neighbors}")