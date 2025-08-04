from tests.test_environment import test_environment_step_verbose
from tests.test_network import (
    test_network_construction,
    test_neighbor_query,
    test_infection_spread
)
from tests.test_attacker import test_attacker_infection_spread
from tests.test_rewards import (
    test_global_reward,
    test_state_reward,
    test_intrinsic_reward
)

if __name__ == "__main__":
    print("\nRunning Environment Test...")
    test_environment_step_verbose()

    print("\n\nRunning Network Tests...")
    test_network_construction()
    test_neighbor_query()
    test_infection_spread()

    print("\n\nRunning Attacker Test...")
    test_attacker_infection_spread()

    print("\n\nRunning Reward Tests...")
    test_global_reward()
    test_state_reward()
    test_intrinsic_reward()

    print("\nAll tests completed.")