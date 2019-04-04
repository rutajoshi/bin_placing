from mdp import *

class AreaReward(Reward):
    """This is a reward function based on the area of the bin covered by objects
    placed in the bin. The returned reward is the fraction of the total bin area
    currently covered by objects that have been placed.
    """
    
    def get_reward(self, state, action, next_state):
        """Returns area-based reward given state, action, and resulting next state.

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
            The fraction of bin area covered by objects already in the bin.

        """
        bin_area = state.bin.area
        old_objects_area, new_objects_area = 0, 0
        for obj in state.objects:
            old_objects_area += obj.polygon.area
        for obj in next_state.objects:
            new_objects_area += obj.polygon.area
        print("\nState objects = " + str(state.objects))
        print("\nNext state objects = " + str(next_state.objects))
        print("\nOld objects area = " + str(old_objects_area))
        print("\nNew objects area = " + str(new_objects_area))
        print("\nBin area = " + str(bin_area))
        result = float(new_objects_area - old_objects_area)/float(bin_area)
        print("\nresult = " + str(result))
        return result
