from mdp import *
from random_policy import *
from rows_policy import *
from heatmap import *
from area_reward import *
from rows_reward import *

# Load the figure with just a bin, then with a bin and a square
def main():
    """This function is the driving function of the bin_packing 2D simulator module.
    It initializes an environment with an initial state and rolls out a policy until
    a termination state is reached.
    """
    
    fig = create_env()
    ax, bin = add_bin(fig, 20, 20)

    policy = RowsPolicy(bin.length, bin.width)
    first_object = PlacementObject.get_random()#Rectangle.get_random(2, 10) #
    while (first_object.polygon.is_valid == False):
        first_object = PlacementObject.get_random() #Rectangle.get_random(2, 10) #
    initial_state = State(bin, [], first_object)
    reward = RowsReward()
    transition = Transition(fig, ax)
    termination = Termination()

    heatmapper = HeatMap()

    rewards = []
    state = initial_state
    while not termination.done(state):
        # heatmapper.generate(state, transition, reward, 1)
        action = policy.get_action(state)
        next_state = transition.execute_action(state, action)
        print("\nPoints of placed object are = " + str(np.array(next_state.objects[-1].bounding_box().polygon.exterior.coords)) + "\n")
        rewards.append(reward.get_reward(state, action, next_state))
        state = next_state

    display_env()


if __name__ == "__main__": main()
