
# ipmsrl_env/node.py
from .constants import NodeState

class Node:
    def __init__(self, node_id, node_type, critical=False):
        self.id = node_id
        self.type = node_type
        self.critical = critical
        self.state = NodeState.HEALTHY
        self.infection_level = 0
        self.alert_triggered = False

    def infect(self):
        if self.state != NodeState.CONTAINED:
            self.infection_level += 1
            self.state = NodeState.INFECTED

    def contain(self):
        self.state = NodeState.CONTAINED

    def eradicate(self):
        self.infection_level = 0
        if self.state == NodeState.INFECTED:
            self.state = NodeState.HEALTHY

    def recover(self):
        if self.infection_level == 0:
            self.state = NodeState.RECOVERED

    def is_infected(self):
        return self.state == NodeState.INFECTED

    def is_contained(self):
        return self.state == NodeState.CONTAINED

    def is_healthy(self):
        return self.state == NodeState.HEALTHY

    def is_recovered(self):
        return self.state == NodeState.RECOVERED