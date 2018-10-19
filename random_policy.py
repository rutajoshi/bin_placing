from mdp import *

class RandomPolicy(Policy):
    def get_action(self, state):
        theta = np.random.uniform(0, 2*np.pi)
        bin_length = state.bin.length
        bin_width = state.bin.width
        transform = np.array([[np.cos(theta), -1*np.sin(theta), np.random.uniform(-bin_size, bin_size)],
                              [np.sin(theta), np.cos(theta), np.random.uniform(-bin_width, bin_width)],
                              [0, 0, 1]])
        action = Action(np.eye(3), state.next_object)
        return action

# TODO:
#   * Add a class for rectangles
#   * Add a bin to the state which is a rectangle
#   * Generate action using the bin length and width
