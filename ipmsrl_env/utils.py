# ipmsrl_env/utils.py
def count_infected_nodes(network):
    return sum(1 for node in network.get_all_nodes() if node.is_infected())

def count_critical_failures(network):
    return sum(1 for node in network.get_all_nodes() if node.critical and node.is_infected())

def log_node_states(network):
    return {
        node.id: {
            'state': node.state.name,
            'infected': node.is_infected(),
            'contained': node.is_contained(),
            'recovered': node.is_recovered(),
            'alert': node.alert_triggered
        }
        for node in network.get_all_nodes()
    }