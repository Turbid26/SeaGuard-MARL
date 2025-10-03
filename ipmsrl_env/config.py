def get_default_config():
    return {
        'nodes': [
            {'id': 'PLC1',  'type': 'PLC',   'critical': True},
            {'id': 'PLC2',  'type': 'PLC',   'critical': True},
            {'id': 'RTU1',  'type': 'RTU',   'critical': True},
            {'id': 'HMI1',  'type': 'HMI',   'critical': False},
            {'id': 'LOP1',  'type': 'LOP',   'critical': False},
            {'id': 'LOP2',  'type': 'LOP',   'critical': False},
            {'id': 'SW1',   'type': 'SWITCH','critical': False},
            {'id': 'SW2',   'type': 'SWITCH','critical': False},
        ],
        'edges': [
            ('PLC1', 'SW1'),
            ('PLC2', 'SW1'),
            ('RTU1', 'SW2'),
            ('HMI1', 'SW1'),
            ('LOP1', 'SW1'),
            ('LOP2', 'SW2'),
            ('SW1',  'SW2')
        ],
        'infection_probability': 0.5,         # 🦠 higher infection chance
        'alert_success_prob': 0.6,            # ❌ less reliable alerts
        'max_timesteps': 50,
        'action_delay': {
            'CONTAIN': 2,                     # ⏱ longer delays
            'ERADICATE': 3,
            'RECOVER': 3
        },
        'reward_weights': {
            'global': 1.0,
            'state': 0.5,
            'intrinsic': 0.2
        }
    }
