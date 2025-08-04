# ipmsrl_env/network.py
import networkx as nx
from .node import Node
from .constants import NodeType

class IPMSNetwork:
    def __init__(self, config):
        self.config = config
        self.graph = nx.Graph()
        self._init_nodes()
        self._init_edges()

    def _init_nodes(self):
        for node_conf in self.config['nodes']:
            node = Node(
                node_id=node_conf['id'],
                node_type=NodeType[node_conf['type']],
                critical=node_conf.get('critical', False)
            )
            self.graph.add_node(node.id, data=node)

    def _init_edges(self):
        for edge in self.config['edges']:
            self.graph.add_edge(*edge)

    def get_node(self, node_id):
        return self.graph.nodes[node_id]['data']

    def neighbors(self, node_id):
        return [self.graph.nodes[n]['data'] for n in self.graph.neighbors(node_id)]

    def spread_infection(self):
        new_infections = []
        for node_id in self.graph.nodes:
            node = self.get_node(node_id)
            if node.is_infected() and not node.is_contained():
                for neighbor in self.neighbors(node_id):
                    if neighbor.is_healthy():
                        new_infections.append(neighbor)

        for node in new_infections:
            node.infect()

    def get_all_nodes(self):
        return [self.get_node(n) for n in self.graph.nodes]
