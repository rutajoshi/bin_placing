from mdp import *

class ConstantReward(Reward):
    def get_reward(self, state, action, next_state):
        if len(next_state.objects) > len(state.objects):
            return 1
        return 0
