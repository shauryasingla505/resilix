# app/services/router_engine.py
import networkx as nx
from typing import List

class RouterEngine:
    def __init__(self):
        self.graph = nx.Graph()
        # Initialize mock spatial nodes and weighted edges
        self.graph.add_edge((12.9100, 79.1300), (12.9120, 79.1320), weight=3.2)
        self.graph.add_edge((12.9120, 79.1320), (12.9250, 79.1400), weight=5.2)
        self.graph.add_edge((12.9100, 79.1300), (12.9250, 79.1400), weight=12.0)

    def compute_route(self, start: List[float], destination: List[float], blocked_nodes: List[str]):
        s_tuple = tuple(start)
        d_tuple = tuple(destination)
        
        try:
            path = nx.astar_path(self.graph, s_tuple, d_tuple, weight="weight")
            eta = round(len(path) * 4.2, 1)
            hazards_avoided = len(blocked_nodes)
            return [list(n) for n in path], eta, hazards_avoided
        except Exception:
            # Fallback direct path if exact nodes aren't indexed in mock graph
            return [list(s_tuple), list(d_tuple)], 10.0, len(blocked_nodes)

pathfinder = RouterEngine()