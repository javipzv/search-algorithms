class Graph:
    def __init__(self, dirigido: bool = False):
        self.graph : dict = {}
        self.dirigido : bool = dirigido

    def add_vertex(self, v: str):
        self.graph[v] = []

    def add_edge(self, v1: str, v2: str, weight: int):
        if v1 not in self.graph:
            self.graph[v1] = []
        if v2 not in self.graph:
            self.graph[v2] = []
        self.graph[v1].append((v2, weight))
        if not self.dirigido:
            self.graph[v2].append((v1, weight))

    def get_vertex(self):
        return [v for v, _ in self.graph.items()]

    def get_neighbors(self, v1: str) -> list:
        return self.graph[v1]
    
    def get_number_of_vertex(self) -> int:
        return len(self.graph)
    
    def show_graph(self):
        for v, neighbors in self.graph.items():
            print(f"{v}: {neighbors}")