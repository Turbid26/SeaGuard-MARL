import sys
import os

# Add the project root to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

from ipmsrl_env.environment import IPMSRLEnv

def env_creator(env_config=None):
    return IPMSRLEnv()

# Register the environment with RLlib
register_env("ipmsrl_env", env_creator)

if __name__ == "__main__":
    ray.init(ignore_reinit_error=True)

    # Create PPO config
    config = (
        PPOConfig()
        .environment("ipmsrl_env")
        .framework("torch")
        .env_runners(
            num_env_runners=1
        )
        .training(gamma=0.99, lr=5e-4, train_batch_size=2000)
    )

    # Train using Tune
    tune.Tuner(
        "PPO",
        run_config=tune.RunConfig(
            stop={"training_iteration": 50},
            verbose=1
        ),
        param_space=config.to_dict()
    ).fit()

    ray.shutdown()
