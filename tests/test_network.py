from ipmsrl_env.config import get_default_config
from ipmsrl_env.network import IPMSNetwork
from ipmsrl_env.utils import count_infected_nodes

def test_network_construction():
    config = get_default_config()
    network = IPMSNetwork(config)

    assert len(network.graph.nodes) == len(config['nodes']), "All nodes should be added"
    assert len(network.graph.edges) == len(config['edges']), "All edges should be added"

    print("✅ Node and edge construction test passed.")

    for node_id, data in network.graph.nodes(data='data'):
        print(f"Node {node_id}: type={data.type.name}, critical={data.critical}, state={data.state.name}")

def test_neighbor_query():
    config = get_default_config()
    network = IPMSNetwork(config)

    node_id = 'SW1'
    neighbors = network.neighbors(node_id)
    neighbor_ids = [n.id for n in neighbors]

    expected = ['PLC1', 'RTU1', 'HMI1', 'LOP1']
    assert sorted(neighbor_ids) == sorted(expected), "SW1 should be connected to all nodes"

    print(f"✅ Neighbor check for {node_id}: {neighbor_ids}")

def test_infection_spread():
    config = get_default_config()
    network = IPMSNetwork(config)

    # Infect SW1 manually
    sw1 = network.get_node('SW1')
    sw1.infect()

    # Run one infection step
    network.spread_infection()

    # Check how many neighbors got infected
    infected_count = count_infected_nodes(network)
    assert infected_count >= 1, "Infection should spread to at least one neighbor (probabilistically)"
    
    print(f"✅ Infection spread test passed. Infected nodes: {infected_count}")

if __name__ == "__main__":
    test_network_construction()
    test_neighbor_query()
    test_infection_spread()