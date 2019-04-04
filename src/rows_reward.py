from mdp import *
from rows_policy import *

class RowsReward(Reward):
    """This is a reward function based on the similarity of an outcome (state, action, next_state)
    to the expected outcome of the RowsPolicy.
    """

    def __init__(self):
        """Initializes a reward function with a saved policy and a dictionary
        of previously seen states mapping to previously used actions. (This is
        metadata for the reward evaluation.)

        Returns
        -------
        RowsReward
            An instance of RowsReward with the above parameters

        """
        self.policy = RowsPolicy(20, 20)
        self.seen_already = dict()

    def get_reward(self, state, action, next_state):
        """Returns RowsPolicy based reward given state, action, and resulting
        next state. If the next_state is the same as the state that would result
        from executing the action returned by RowsPolicy, the reward is 1.

        If the action places the next object on top of other objects in the bin,
        or outside the bin/in collision with it, the reward is 0.

        Otherwise the reward is 1.0 / (distance between this action and RowsPolicy action)

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
            A function of the distance between the input action and the action suggested by
            RowsPolicy.

        """
        if (state in self.seen_already):
            rows_action = self.seen_already[state]
        else:
            rows_action = self.policy.get_action(state)
            self.seen_already[state] = rows_action

        # Compute the distance between the rows_next_action and the action
        rows_translation = rows_action.translation
        action_translation = action.translation
        dist = np.linalg.norm(rows_translation - action_translation)

        # # If the action puts the new object outside the bin, return 0
        obj_copy = state.next_object.copy()
        obj_copy.apply_transform(action.transform)

        # Use np.all_close instead of equals comparison for floating point
        print("Intersecting: " + str(intersecting(obj_copy, state.bin))  + "\n")
        print("Polygon area: " + str(obj_copy.polygon.area)  + "\n")
        print("Valid = " + str(obj_copy.polygon.is_valid) + "\n")

        if (obj_copy.polygon.is_valid and intersecting(obj_copy, state.bin) < obj_copy.polygon.area):
            return 0
        #
        # # If the action puts the new object on top of an object in the bin, return 0
        for o in state.objects:
            if (obj_copy.polygon.is_valid and o.polygon.is_valid and intersecting(obj_copy, o) != 0):
                return 0

        if dist == 0:
            return 1

        return 1.0 / dist
