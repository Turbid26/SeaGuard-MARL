
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
        self.contained = False  # NEW
        self.infected = False   # NEW

    def infect(self):
        if not self.contained:
            self.infection_level += 1
            self.state = NodeState.INFECTED
            self.infected = True

    def contain(self):
        self.contained = True
        self.state = NodeState.CONTAINED

    def eradicate(self):
        self.infection_level = 0
        self.infected = False
        if self.state == NodeState.INFECTED or self.state == NodeState.CONTAINED:
            self.state = NodeState.HEALTHY
        self.contained = False

    def recover(self):
        if self.infection_level == 0:
            self.state = NodeState.RECOVERED
            self.infected = False
            self.contained = False

    def is_infected(self):
        return self.infected

    def is_contained(self):
        return self.contained

    def is_healthy(self):
        return not self.infected and not self.contained

    def is_recovered(self):
        return self.state == NodeState.RECOVERED
