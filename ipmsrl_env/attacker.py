# ipmsrl_env/attacker.py
import random

class Attacker:
    def __init__(self, network, config):
        self.network = network
        self.config = config
        self.alert_success_prob = config['alert_success_prob']

    def step(self):
        for node in self.network.get_all_nodes():
            if node.is_infected() and not node.is_contained():
                for neighbor in self.network.neighbors(node.id):
                    if neighbor.is_healthy() and self._should_infect():
                        neighbor.infect()
                        if self._should_alert():
                            neighbor.alert_triggered = True

    def _should_infect(self):
        return random.random() < self.config['infection_probability']

    def _should_alert(self):
        return random.random() < self.alert_success_prob
