from mdp import *

class RandomPolicy(Policy):
    """This is a random policy that places an object anywhere in the bin,
    rotated at any angle in 2 dimensions.
    """

    def get_action(self, state):
        """Returns an action uniformly at random given the state. The angle of
        rotation and the translation are sampled uniformly at random given the
        bin dimensions.

        Parameters
        ----------
        state       : State
            Starting state

        Returns
        -------
        action      : Action
            An action to take from this state.

        """
        theta = np.random.uniform(0, 2*np.pi)
        bin_length = state.bin.length
        bin_width = state.bin.width
        transform = np.array([[np.cos(theta), -1*np.sin(theta), np.random.uniform(-bin_length/2, bin_length/2)],
                              [np.sin(theta), np.cos(theta), np.random.uniform(-bin_width/2, bin_width/2)],
                              [0, 0, 1]])
        action = Action(transform, state.next_object)
        return action
