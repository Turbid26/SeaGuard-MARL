
# ipmsrl_env/config.py
def get_default_config():
    return {
        'nodes': [
            {'id': 'PLC1', 'type': 'PLC', 'critical': True},
            {'id': 'RTU1', 'type': 'RTU', 'critical': True},
            {'id': 'HMI1', 'type': 'HMI', 'critical': False},
            {'id': 'LOP1', 'type': 'LOP', 'critical': False},
            {'id': 'SW1', 'type': 'SWITCH', 'critical': False},
        ],
        'edges': [
            ('PLC1', 'SW1'),
            ('RTU1', 'SW1'),
            ('HMI1', 'SW1'),
            ('LOP1', 'SW1')
        ],
        'infection_probability': 0.3,
        'alert_success_prob': 0.9,
        'max_timesteps': 50,
        'action_delay': {
            'CONTAIN': 1,
            'ERADICATE': 2,
            'RECOVER': 2
        },
        'reward_weights': {
            'global': 1.0,
            'state': 0.5,
            'intrinsic': 0.2
        }
    }
