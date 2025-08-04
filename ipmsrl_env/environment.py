# ipmsrl_env/environment.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from .config import get_default_config
from .network import IPMSNetwork
from .attacker import Attacker
from .defender import Defender
from .rewards import calculate_global_reward, calculate_state_reward, calculate_intrinsic_reward
from .constants import ActionType

class IPMSRLEnv(gym.Env):
    def __init__(self, env_config = None):

        super().__init__()
        self.config = get_default_config() if env_config is None else env_config
        
        self.config = get_default_config()
        self.network = IPMSNetwork(self.config)
        self.attacker = Attacker(self.network, self.config)
        self.defender = Defender(self.network)
        self.timesteps = 0
        self.max_timesteps = self.config['max_timesteps']

        # One action per node
        self.action_space = spaces.MultiDiscrete([len(ActionType)] * len(self.network.graph.nodes))
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(len(self.network.get_all_nodes()) * 3,),  # 3 features per node
            dtype=np.float32
        )
    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)

        self.network = IPMSNetwork(self.config)
        self.attacker = Attacker(self.network, self.config)
        self.defender = Defender(self.network)
        self.timesteps = 0

        return self._get_flat_obs(), {}

    def step(self, actions):
        rewards = 0
        self.timesteps += 1

        # Defender actions
        for idx, node in enumerate(self.network.get_all_nodes()):
            action = ActionType(actions[idx])
            self.defender.act(node, action)
            rewards += self.config['reward_weights']['intrinsic'] * calculate_intrinsic_reward(action, node)

        # Attacker step
        self.attacker.step()

        # Rewards
        rewards += self.config['reward_weights']['state'] * calculate_state_reward(self.network)
        rewards += self.config['reward_weights']['global'] * calculate_global_reward(self.network)

        done = self.timesteps >= self.max_timesteps or calculate_global_reward(self.network) != 0
        obs = self._get_flat_obs()

        return obs, rewards, done, False, {}

    def _get_flat_obs(self):
        obs = []
        for node in self.network.get_all_nodes():
            obs.append(int(node.is_infected()))
            obs.append(int(node.is_contained()))
            obs.append(int(node.alert_triggered))

        return np.array(obs, dtype=np.float32)