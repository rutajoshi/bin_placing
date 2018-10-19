from utils import *
from objects import *

class State:
    def __init__(self, bin, objects, next_object):
        self.bin = bin
        self.objects = objects
        self.next_object = next_object

    def copy(self):
        new_state = State(self.bin, self.objects, self.next_object)
        return new_state

class Action:
    def __init__(self, transform, next_object):
        self.transform = transform
        self.rotation = transform[:2,:2]
        self.translation = transform[:2,2]
        self.next_object = next_object

class Policy:
    def __init__(self, bin_length, bin_width):
        self.bin_length = bin_length
        self.bin_width = bin_width

    def get_action(self, state):
        action = Action(np.eye(3), state.next_object)
        return action

class Reward:
    def get_reward(self, state, action, next_state):
        if len(next_state.objects) > len(state.objects):
            return 1
        return 0

class Transition:
    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax

    def execute_action(self, state, action):
        next_state = state.copy()
        action.next_object.apply_transform(action.transform)
        add_object(self.fig, self.ax, action.next_object)
        next_state.objects.append(action.next_object)
        # Pick a new next object
        next_state.next_object = Square(5, np.eye(3))
        return next_state

class Termination:
    def done(self, state):
        # Go through the objects pairwise and return True if any overlap
        # Also return True if any object is outside the bin
        for objA in state.objects:
            bin_contained = intersecting(objA, state.bin)
            if (bin_contained < objA.polygon.area):
                print("Bin contained = " + str(bin_contained) + " < polygon area = " + str(objA.polygon.area))
                return True
            for objB in [i for i in state.objects if i != objA]:
                if intersecting(objA, objB) > 0:
                    print("Object " + str(np.array(objA.polygon.exterior.coords)) + " intersects " + str(np.array(objB.polygon.exterior.coords)))
                    return True
        return False
