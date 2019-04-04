from mdp import *

class ConstantReward(Reward):
    """This is a reward function that returns a constant binary result.
    """
    def get_reward(self, state, action, next_state):
        """Returns constant reward given state, action, and resulting next state.

        Parameters
        ----------
        state       : State
            Starting state
        action      : Action
            Action given by policy
        next_state  : State
            State resulting from applying action to state

        Returns
        -------
        float
            1 if an object was added to the bin, 0 if no objects were added.

        """
        if len(next_state.objects) > len(state.objects):
            return 1
        return 0
