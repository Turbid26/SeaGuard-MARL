
from ipmsrl_env.environment import IPMSRLEnv
from ipmsrl_env.utils import log_node_states
import numpy as np
import pprint

def test_environment_step_verbose():
    env = IPMSRLEnv()
    obs = env.reset()
    
    print("Initial Observation:")
    pprint.pprint(obs)

    assert isinstance(obs, dict), "Observation should be a dict"
    assert len(obs) == len(env.network.get_all_nodes()), "Should have one observation per node"

    actions = [3] * len(env.network.get_all_nodes())  # WAIT = 3
    obs, reward, done, info = env.step(actions)

    print("\nAfter Step:")
    print(f"Reward: {reward}")
    print(f"Done: {done}")
    print("New Observation:")
    pprint.pprint(obs)

    print("\nNode States:")
    node_states = log_node_states(env.network)
    pprint.pprint(node_states)

    assert isinstance(reward, float), "Reward should be float"
    assert isinstance(done, bool), "Done should be bool"
    assert isinstance(obs, dict), "Observation should be dict"
    assert isinstance(info, dict), "Info should be dict"

    print("\nTest passed: environment.step() works as expected with detailed output.")

if __name__ == "__main__":
    test_environment_step_verbose()