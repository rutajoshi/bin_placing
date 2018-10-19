from mdp import *
from random_policy import *

# Load the figure with just a bin, then with a bin and a square
def main():
    fig = create_env()
    ax, bin = add_bin(fig, 20, 20)

    policy = RandomPolicy(bin.length, bin.width)
    first_object = Square(5, np.eye(3))
    initial_state = State(bin, [], first_object)
    reward = Reward()
    transition = Transition(fig, ax)
    termination = Termination()

    rewards = []
    state = initial_state
    while not termination.done(state):
        action = policy.get_action(state)
        next_state = transition.execute_action(state, action)
        rewards.append(reward.get_reward(state, action, next_state))
        state = next_state
    display_env()


if __name__ == "__main__": main()
