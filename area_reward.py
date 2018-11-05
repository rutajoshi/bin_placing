from mdp import *

class AreaReward(Reward):
    def get_reward(self, state, action, next_state):
        bin_area = state.bin.area
        old_objects_area, new_objects_area = 0, 0
        for obj in state.objects:
            old_objects_area += obj.polygon.area
        for obj in next_state.objects:
            new_objects_area += obj.polygon.area
        return float(new_objects_area - old_objects_area)/float(bin_area)
