from utils import *
from objects import *
from shapely.geometry import Point

# def smoothListGaussian(list,degree=5):
#      window=degree*2-1
#      weight=np.array([1.0]*window)
#      weightGauss=[]
#      for i in range(window):
#          i=i-degree+1
#          frac=i/float(window)
#          gauss=1/(np.exp((4*(frac))**2))
#          weightGauss.append(gauss)
#      weight=np.array(weightGauss)*weight
#      smoothed=[0.0]*(len(list)-window)
#      for i in range(len(smoothed)):
#          smoothed[i]=sum(np.array(list[i:i+window])*weight)/sum(weight)
#      return smoothed
#
# def generate_random(number, polygon):
#     minx, miny, maxx, maxy = polygon.bounds
#     theta = np.linspace(0, 2*np.pi, number, endpoint=False)
#     r = np.random.lognormal(0,1.5,number)
#     r = np.pad(r,(9,10),mode='wrap')
#     r = smoothListGaussian(r, degree=10)
#     coords = zip(np.cos(theta)*r, np.sin(theta)*r)
#     # coords = [i for i in coords if minx < i[0] < maxx and miny < i[1] < maxy]
#     # polygon = Polygon(coords)
#     return coords

class State:
    def __init__(self, bin, objects, next_object):
        self.bin = bin
        self.objects = objects
        self.next_object = next_object

    def copy(self):
        bin_copy = self.bin.copy()
        obj_copy = [o for o in self.objects]
        next_obj_copy = self.next_object.copy()
        # new_state = State(self.bin, self.objects, self.next_object)
        new_state = State(bin_copy, obj_copy, next_obj_copy)
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

    def try_transitioning(self, state, action, add_to_sim=True):
        next_state = state.copy()
        next_object = action.next_object.copy()
        next_object.apply_transform(action.transform)
        if (add_to_sim):
            add_object(self.fig, self.ax, next_object)
        next_state.objects.append(next_object)
        # Pick a new next object
        # next_state.next_object = Square(5, np.eye(3))
        next_state.next_object = Rectangle.get_random(2, 10)
        while (next_state.next_object.polygon.is_valid == False):
            next_state.next_object = Rectangle.get_random(2, 10)
        return next_state

    def execute_action(self, state, action, add_to_sim=True):
        next_state = state.copy()
        action.next_object.apply_transform(action.transform)
        if (add_to_sim):
            add_object(self.fig, self.ax, action.next_object.bounding_box())
        next_state.objects.append(action.next_object)
        # Pick a new next object
        # next_state.next_object = Square(5, np.eye(3))
        next_state.next_object = PlacementObject.get_random()#Rectangle.get_random(2, 10)
        while (next_state.next_object.polygon.is_valid == False):
            next_state.next_object = PlacementObject.get_random() #Rectangle.get_random(2, 10)
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

class Value:
    def evaluate(self, state):
        return 0
