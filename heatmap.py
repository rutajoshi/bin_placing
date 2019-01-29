# Generates a heatmap of possible placements.

from mdp import *
import matplotlib.pyplot as plt

class HeatMap:
    def generate(self, state, transition, reward, num_rotations):
        # Generate a heat map and display it

        # Get bounding box of the state's next object
        aabb = state.next_object.bounding_box()
        for i in range(num_rotations):
            theta = i * (2*np.pi / num_rotations)
            # print("Bin length = " + str(state.bin.length) + "\nBin width = " + str(state.bin.width) + "\n")
            # print("AABB length = " + str(aabb.length) + "\nAABB width = " + str(aabb.width) + "\n")
            horiz = int(state.bin.length - aabb.length) #int(state.bin.length // aabb.length)
            vert = int(state.bin.width - aabb.width) #int(state.bin.width // aabb.width)
            print("\nHoriz = " + str(horiz) + "\nVert = " + str(vert) + "\n")
            rewards = np.array([[1.0 for i in range(horiz)] for j in range(vert)])

            for y in range(vert):
                for x in range(horiz):
                    # Compute reward for an action that places the target object here
                    transform = np.array([[np.cos(theta), -1*np.sin(theta), x],
                                          [np.sin(theta), np.cos(theta), y],
                                          [0, 0, 1]])
                    action = Action(transform, state.next_object.copy())
                    next_state = transition.try_transitioning(state, action, add_to_sim=False)
                    r = reward.get_reward(state, action, next_state)
                    # print("\nr = " + str(r))
                    rewards[y][x] = r

            print("\nRewards = " + str(rewards) + "\n")
            plt.imshow(rewards, cmap='hot', interpolation='nearest')
            plt.show()
        # Divide the bin area to get a grid of locations
        # For each of n rotations of the object, generate a heatmap and display it

        # Go through all possible actions and evaluate reward function
        # Put these into a matrix and plot it as a heat map
