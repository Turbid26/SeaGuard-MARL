
from ipmsrl_env.config import get_default_config
from ipmsrl_env.network import IPMSNetwork
from ipmsrl_env.attacker import Attacker
from ipmsrl_env.utils import count_infected_nodes, log_node_states
import pprint

def test_attacker_infection_spread():
    config = get_default_config()
    config['infection_probability'] = 1.0  # Force infection for test
    config['alert_success_prob'] = 1.0     # Force alert triggering

    network = IPMSNetwork(config)
    attacker = Attacker(network, config)

    # Infect SW1 manually
    sw1 = network.get_node('SW1')
    sw1.infect()

    print("\n🔬 Before attack step:")
    pprint.pprint(log_node_states(network))

    attacker.step()

    print("\n⚠️ After attack step:")
    pprint.pprint(log_node_states(network))

    infected = count_infected_nodes(network)
    assert infected > 1, f"Expected more than 1 infected node, got {infected}"

    alerts_triggered = sum(1 for n in network.get_all_nodes() if n.alert_triggered)
    assert alerts_triggered >= 1, "At least one alert should have triggered"

    print(f"\n✅ Attacker infection spread test passed. Infected: {infected}, Alerts: {alerts_triggered}")

if __name__ == "__main__":
    test_attacker_infection_spread()