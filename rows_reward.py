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

        # If the action puts the new object outside the bin, return a large number
        obj_copy = state.next_object.copy()
        obj_copy.apply_transform(action.transform)
        if (obj_copy.polygon.is_valid and intersecting(obj_copy, state.bin) < obj_copy.polygon.area):
            print("Here yo\n")
            print("Bin coords = " + str(state.bin.polygon.exterior) + "\n")
            print("Next object coords = " + str(obj_copy.polygon.exterior) + "\n")
            print("Intersection = " + str(intersecting(obj_copy, state.bin)) + "\n")
            print("Area of obj_copy = " + str(obj_copy.polygon.area) + "\n")
            return state.bin.width * state.bin.length

        # If the action puts the new object on top of an object in the bin, return a large number
        for o in state.objects:
            if (obj_copy.polygon.is_valid and o.polygon.is_valid and intersecting(obj_copy, o) != 0):
                print("Well bummer\n")
                return state.bin.width * state.bin.length

        return dist
