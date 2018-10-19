from utils import *
from objects import *

class State:
    def __init__(self, bin, objects, next_object):
        self.bin = bin
        self.objects = objects
        self.next_object

class Action:
    def __init__(self, transform, next_object):
        self.transform = transform
        self.rotation = transform[:2,:2]
        self.translation = transform[:2,2]
        self.next_object = next_object

    def execute(self, fig, ax):
        self.next_object.apply_transform(self.transform)
        assert(ENV_CREATED)
        add_object(fig, ax, self.next_object)


class Policy:
    def __init__(self, bin_size):
        self.bin_size = bin_size

    def get_action(self, state):
        action = Action(np.eye(3), state.next_object)
        return action

class Reward:
    def get_reward(self, state, action, next_state):
        return 0
