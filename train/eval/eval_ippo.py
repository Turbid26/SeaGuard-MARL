import sys
import os
import numpy as np

# Add root to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT_DIR)


from ray.rllib.algorithms.ppo import PPO, PPOConfig
from ray.tune.registry import register_env
from ipmsrl_env.environment import IPMSRLEnv
from ipmsrl_env.utils import log_node_states

import torch
from torch.distributions import Categorical

register_env("ipmsrl_env", lambda cfg: IPMSRLEnv(cfg))
# Add this function
def create_eval_algorithm(checkpoint_path):
    config = (
        PPOConfig()
        .environment(IPMSRLEnv)
        .framework("torch")
        .env_runners(num_env_runners=1)
    )
    algo = PPO(config=config).from_checkpoint(checkpoint_path)
    return algo

# ✅ Provide full path to your trained checkpoint
CHECKPOINT_PATH = r"C:\Users\Raghu\ray_results\PPO_2025-08-04_11-46-31\PPO_ipmsrl_env_90a41_00000_0_2025-08-04_11-46-32\checkpoint_000000"

def evaluate(checkpoint_path):

    print("🚀 Loading trained policy from:", checkpoint_path)
    algo = create_eval_algorithm(checkpoint_path)


    env = IPMSRLEnv()
    obs, _ = env.reset()

    total_reward = 0
    done = False
    step = 0

    print("\n🎯 Running evaluation episode:\n")

    module = algo.get_module()
    dist_class = module.get_exploration_action_dist_cls()

    while not done:
        obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)

        # Inference
        output = module.forward_inference({"obs": obs_tensor})
        logits = output["action_dist_inputs"][0]  # remove batch dim: shape (20,)

        # Split logits for each categorical action (4 per node)
        split_logits = torch.split(logits, 4)  # 4 logits per action dim
        action_dist = dist_class(list(split_logits))

        # Sample full action vector
        actions = [Categorical(logits=logit_group).sample().item() for logit_group in split_logits]

        obs, reward, done, _, _ = env.step(actions)
        total_reward += reward
        step += 1

        print(f"Step {step}: reward={reward:.2f}, done={done}")
        state_log = log_node_states(env.network)
        for node_id, info in state_log.items():
            print(f"  {node_id}: {info}")

    print("\n✅ Evaluation complete.")
    print(f"🏁 Total reward: {total_reward:.2f}")
    print(f"📏 Steps: {step}")

if __name__ == "__main__":
    evaluate(CHECKPOINT_PATH)