
# ipmsrl_env/defender.py
from .constants import ActionType

class Defender:
    def __init__(self, network):
        self.network = network

    def observe(self):
        obs = {}
        for node in self.network.get_all_nodes():
            obs[node.id] = {
                'infected': node.is_infected(),
                'contained': node.is_contained(),
                'alert': node.alert_triggered
            }
        return obs

    def act(self, node, action):
        if action == ActionType.CONTAIN:
            node.contain()
        elif action == ActionType.ERADICATE:
            node.eradicate()
        elif action == ActionType.RECOVER:
            node.recover()
        # WAIT is a no-op
