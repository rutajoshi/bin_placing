# Generates a heatmap of possible placements.

from mdp import *
import matplotlib.pyplot as plt

class HeatMap:
    """This is a class to generate a heat map given a state, transition, reward
    function, and a number of rotations. It rotates an object and generates actions
    which are placement transforms across a grid overlaid on the bin. It then
    evaluates the reward function at each of these and creates a heatmap out of
    the rewards.
    """
    def generate(self, state, transition, reward, num_rotations):
        """Generates a heat map of rewards:
        1) Divide the bin area to get a grid of locations
        2) For each of n rotations of the object, generate a heatmap and display it

        3) Go through all possible actions and evaluate reward function
        4) Put these into a matrix and plot it as a heat map

        Parameters
        ----------
        state           : State
            Starting state
        transition      : Transition
            Transition object for applying actions tested in this method
        reward          : Reward
            Reward function used to generate heatmap
        num_rotations   : int
            Number of rotations of the target object to consider

        Returns
        -------
        None
            Nothing is returned. A heatmap is displayed.

        """
        for i in range(num_rotations):
            # Get rotation angle
            theta = i * (2*np.pi / num_rotations)

            rewards = np.array([[1.0 for i in range(state.bin.length)] for j in range(state.bin.width)])

            for y in range(int(-state.bin.width/2), int(state.bin.width/2)):
                for x in range(int(-state.bin.length/2), int(state.bin.length/2)):
                    # Compute reward for an action that places the target object here
                    obj_copy = state.next_object.copy()
                    current_pos = obj_copy.get_transform()[:2,2]
                    transform = np.array([[np.cos(theta), -1*np.sin(theta), x - current_pos[0]],
                                          [np.sin(theta), np.cos(theta), y - current_pos[1]],
                                          [0, 0, 1]])
                    action = Action(transform, obj_copy)
                    next_state = transition.try_transitioning(state, action, add_to_sim=False)
                    r = reward.get_reward(state, action, next_state)
                    # print("\nr = " + str(r))
                    rewards[y + int(state.bin.width/2)][x + int(state.bin.length/2)] = r

            print("\nRewards = " + str(rewards) + "\n")
            plt.imshow(rewards, cmap='hot', interpolation='nearest')
            plt.show()
