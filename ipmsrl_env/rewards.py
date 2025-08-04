# ipmsrl_env/rewards.py
def calculate_global_reward(network):
    critical_nodes = [n for n in network.get_all_nodes() if n.critical]
    if any(n.is_infected() for n in critical_nodes):
        return -1.0  # loss
    elif all(not n.is_infected() and not n.is_contained() for n in network.get_all_nodes()):
        return 1.0  # win
    return 0.0  # draw

def calculate_state_reward(network):
    penalty = 0
    for node in network.get_all_nodes():
        if node.is_infected():
            penalty -= 1 if node.critical else 0.5
        elif node.is_contained() and not node.is_infected():
            penalty -= 0.2
    return penalty

def calculate_intrinsic_reward(action, node):
    if action.name == 'WAIT':
        return 0
    if action.name == 'CONTAIN' and not node.is_infected():
        return -0.3
    if action.name == 'ERADICATE' and not node.is_infected():
        return -0.5
    if action.name == 'RECOVER' and node.is_infected():
        return -0.7
    return 0.1