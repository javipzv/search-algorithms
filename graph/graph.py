from shapely import LineString

class Vertex:
    """
    Class to represent a vertex in a graph
    """
    def __init__(self, id: str, latitude: float, longitude: float) -> None:
        """
        Constructor of the class
        """
        self.id: str = id
        self.latitude: float = latitude
        self.longitude: float = longitude

    def __eq__(self, other: object) -> bool:
        """
        Method to compare two vertices
        """
        if isinstance(other, Vertex):
            return self.id == other.id
        return False
    
    def __lt__(self, other: 'Vertex') -> bool:
        """
        Method to declare the order of the vertices
        """
        return self.id < other.id

    def __hash__(self) -> int:
        """
        Method to hash the vertex
        """
        return hash(self.id)

class Edge:
    def __init__(self, source_id, destination_id, weight, linestring) -> None:
        """
        Constructor of the class
        """
        self.source_id: int = source_id
        self.destination_id: int = destination_id
        self.weight: float = weight
        self.linestring: LineString = linestring
    
    def __eq__(self, other: object) -> bool:
        """
        Method to compare two edges
        """
        if isinstance(other, Edge):
            return self.source_id == other.source_id and self.destination_id == other.destination_id or \
                    self.source_id == self.destination_id and self.destination_id == other.source_id
        return False

    def __lt__(self, other: 'Vertex') -> bool:
        """
        Method to declare the order of the edges
        """
        return self.source_id + self.destination_id < other.source_id + other.destination_id

    def __hash__(self) -> int:
        """
        Method to hash the edge
        """
        return hash((self.source_id, self.destination_id))

class Graph:
    """
    Class to represent a graph
    """
    def __init__(self, dirigido: bool = False):
        """
        Constructor of the class
        """
        self.graph: dict = {}
        self.vertices: dict = {}
        self.edges: dict = {}
        self.dirigido: bool = dirigido

    def add_vertex(self, v: Vertex):
        """
        Method to add a vertex to the graph
        """
        self.graph[v] = []
        self.vertices[v.id] = v

    def add_edge(self, v1: Vertex, v2: Vertex, weight: int, linestring):
        """
        Method to add an edge to the graph
        """
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

    def get_edge_by_vertices(self, v1: Vertex, v2: Vertex) -> Edge:
        """
        Method to get an edge by its vertices
        """
        return self.edges[(min(v1.id, v2.id), max(v1.id, v2.id))]

    def get_vertices(self) -> list[Vertex]:
        """
        Method to get the vertices of the graph
        """
        return [vertex for vertex, _ in self.graph.items()]

    def get_vertex_by_id(self, id) -> Vertex:
        """
        Method to get a vertex by its id
        """
        return self.vertices[id] if id in self.vertices else None

    def get_neighbors(self, v1: Vertex) -> list[Vertex]:
        """
        Method to get the neighbors of a vertex
        """
        return self.graph[v1]