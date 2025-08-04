from ipmsrl_env.config import get_default_config
from ipmsrl_env.network import IPMSNetwork
from ipmsrl_env.rewards import (
    calculate_global_reward,
    calculate_state_reward,
    calculate_intrinsic_reward
)
from ipmsrl_env.constants import ActionType

def test_global_reward():
    config = get_default_config()
    network = IPMSNetwork(config)

    # Case 1: All healthy
    assert calculate_global_reward(network) == 1.0, "Should be win initially (All healthy)"

    # Case 2: Infect a critical node
    plc1 = network.get_node('PLC1')
    plc1.infect()
    assert calculate_global_reward(network) == -1.0, "Should be loss if critical is infected"

    # Case 3: All nodes recovered (no infection or containment)
    plc1.eradicate()
    for node in network.get_all_nodes():
        node.recover()
    assert calculate_global_reward(network) == 1.0, "Should be win if all nodes healthy and recovered"

    print("✅ Global reward logic passed.")

def test_state_reward():
    config = get_default_config()
    network = IPMSNetwork(config)

    plc1 = network.get_node('PLC1')
    hmi1 = network.get_node('HMI1')

    plc1.infect()  # critical
    hmi1.infect()  # non-critical

    print(f"HMI1 state before containment: INFECTED={hmi1.is_infected()}, CONTAINED={hmi1.is_contained()}")
    reward = calculate_state_reward(network)

    print(f"State reward (2 infected): {reward}")
    assert reward < 0, "Should penalize infection"

    hmi1.contain()

    print(f"HMI1 state after containment: INFECTED={hmi1.is_infected()}, CONTAINED={hmi1.is_contained()}")
    reward2 = calculate_state_reward(network)
    print(f"State reward (with containment): {reward2}")
    print(f"Reward before: {reward}, after containment: {reward2}")
    
    assert reward2 == reward, "Containment of infected node should not change state reward"

    print("✅ State reward logic passed.")

def test_intrinsic_reward():
    config = get_default_config()
    network = IPMSNetwork(config)
    node = network.get_node('HMI1')

    # Correct use: contain infected node
    node.infect()
    r1 = calculate_intrinsic_reward(ActionType.CONTAIN, node)
    assert r1 >= 0, "Containing infected node should not be penalized"

    # Incorrect: eradicate healthy node
    node.eradicate()
    r2 = calculate_intrinsic_reward(ActionType.ERADICATE, node)
    assert r2 < 0, "Eradicating healthy node should be penalized"

    # Incorrect: recover infected node
    node.infect()
    r3 = calculate_intrinsic_reward(ActionType.RECOVER, node)
    assert r3 < 0, "Recovering infected node should be penalized"

    # Wait is neutral
    r4 = calculate_intrinsic_reward(ActionType.WAIT, node)
    assert r4 == 0, "WAIT should be neutral"

    print("✅ Intrinsic reward logic passed.")

if __name__ == "__main__":
    test_global_reward()
    test_state_reward()
    test_intrinsic_reward()
