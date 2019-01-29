from mdp import *
from rows_policy import *

class RowsReward(Reward):
    def __init__(self):
        self.policy = RowsPolicy(20, 20)

    def get_reward(self, state, action, next_state):
        rows_action = self.policy.get_action(state)
        # Compute the distance between the rows_next_action and the action
        rows_translation = rows_action.translation
        action_translation = action.translation
        dist = np.linalg.norm(rows_translation - action_translation)
        return dist
