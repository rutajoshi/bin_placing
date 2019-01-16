from mdp import *

class AreaReward(Reward):
    def get_reward(self, state, action, next_state):
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
