# ipmsrl_env/constants.py
from enum import Enum, auto

class NodeType(Enum):
    PLC = auto()
    RTU = auto()
    HMI = auto()
    LOP = auto()
    SWITCH = auto()

class NodeState(Enum):
    HEALTHY = auto()
    INFECTED = auto()
    CONTAINED = auto()
    RECOVERED = auto()

class ActionType(Enum):
    CONTAIN = 0
    ERADICATE = 1
    RECOVER = 2
    WAIT = 3
