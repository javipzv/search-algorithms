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

class Graph:
    def __init__(self, dirigido: bool = False):
        self.graph : dict = {}
        self.dirigido : bool = dirigido

    def add_vertex(self, v: Vertex):
        self.graph[v] = []

    def add_edge(self, v1: Vertex, v2: Vertex, weight: int):
        if v1 not in self.graph:
            self.graph[v1] = []
        if v2 not in self.graph:
            self.graph[v2] = []
        self.graph[v1].append((v2, weight))
        if not self.dirigido:
            self.graph[v2].append((v1, weight))

    def get_vertices(self):
        return [v for v, _ in self.graph.items()]

    def get_neighbors(self, v1: Vertex) -> list:
        return self.graph[v1]
    
    def get_number_of_vertex(self) -> int:
        return len(self.graph)
    
    def show_graph(self):
        for v, neighbors in self.graph.items():
            print(f"{v}: {neighbors}")