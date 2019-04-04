from utils import *
from objects import *
import math

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
    """This class is the state representation for the bin placing project.
    A bin placing state contains:
    1) a bin
    2) a list of objects
    3) an object which will be placed next
    
    """

    def __init__(self, bin, objects, next_object):
        """Initializes a state, given the bin, list of objects, and next object.

        Parameters
        ----------
        bin       : Rectangle
            The object representation of the placement bin
        objects   : list
            A list of PlacementObjects already placed in the bin
        next_object  : PlacementObject
            The next PlacementObject that will be placed in the bin

        Returns
        -------
        State
            An instance of State with the above parameters

        """
        self.bin = bin
        self.objects = objects
        self.next_object = next_object

    def copy(self):
        """Creates and returns a copy of this state. The bin and next_object are
        replicated, but the list of objects is a shallow copy (a new list, but the
        same objects).

        Returns
        -------
        State
            A copy of this instance of State

        """
        bin_copy = self.bin.copy()
        obj_copy = [o for o in self.objects]
        next_obj_copy = self.next_object.copy()
        # new_state = State(self.bin, self.objects, self.next_object)
        new_state = State(bin_copy, obj_copy, next_obj_copy)
        return new_state

class Action:
    """This class is the action representation for the bin placing project.
    A bin placing action contains:
    1) a transform from origin in world space coordinates (3x3 translation
       and rotation matrix)
    2) a next object to be placed using the transform

    """

    def __init__(self, transform, next_object):
        """Initializes an action, given the transform and next object.

        Parameters
        ----------
        transform       : numpy array (3,3)
            A homogenous coordinates transformation matrix which is 3x3 (2x2 rotation, 2x1 translation)
        next_object  : PlacementObject
            The next PlacementObject that will be placed in the bin using transform

        Returns
        -------
        Action
            An instance of Action with the above parameters

        """
        self.transform = transform
        self.rotation = transform[:2,:2]
        self.translation = transform[:2,2]
        self.next_object = next_object

class Policy:
    """This is a parent class for policies for the bin placing project.
    A bin placing policy contains:
    1) a bin length
    2) a bin width

    """

    def __init__(self, bin_length, bin_width):
        """Initializes a policy given bin dimensions. This is a parent class for
        actual policies, and should not be used in practice. The get_action method
        for this parent class returns the identity transform on the input state's
        next_object.

        Parameters
        ----------
        bin_length  : int
            Bin length dimension (x)
        bin_width   : int
            Bin width dimension (y)

        Returns
        -------
        Policy
            An instance of Policy with the above parameters

        """
        self.bin_length = bin_length
        self.bin_width = bin_width

    def get_action(self, state):
        """Returns an action given a state by executing the policy. Since this is
        the parent class, the action is the identity transform on the state's next_object.

        Parameters
        ----------
        state   : State
            Current state of the environment

        Returns
        -------
        Action
            An action that the policy dictates to be the best action. (Identity for this parent class)

        """
        action = Action(np.eye(3), state.next_object)
        return action

class Reward:
    """This is a parent class for reward functions for the bin placing project.
    A bin placing reward contains only a function that returns the evaluation of
    the reward function given state, action, and next_state.

    """

    def get_reward(self, state, action, next_state):
        """Returns the evaluation of the reward function given a state, action,
        and next_state.

        Parameters
        ----------
        state       : State
            Current state of the environment
        action      : Action
            Action taken from the state
        next_state  : State
            State of the environment resulting from execution of the action

        Returns
        -------
        float
            The reward for getting from state to next_state via action. For
            this parent class, return constant reward (1 if an object was placed,
            0 otherwise)

        """
        if len(next_state.objects) > len(state.objects):
            return 1
        return 0

class Transition:
    """This is a representation of transitions for the bin placing project.
    A bin placing transition contains:
    1) a figure for the environment
    2) axes for the bin

    """

    def __init__(self, fig, ax):
        """Initializes a transition given plotting environment parameters (matplotlib figures).

        Parameters
        ----------
        fig : matplotlib.pyplot.Figure
            Figure used to display the bin and objects
        ax  : an matplotlib.axes.SubplotBase subclass of Axes (or a subclass of Axes)
            The axes of the subplot corresponding to the bin

        Returns
        -------
        Transition
            An instance of Transition with the above parameters

        """
        self.fig = fig
        self.ax = ax

    def try_transitioning(self, state, action, add_to_sim=True):
        """Generates a copy of the action's next_object to be placed, executes
        the action on that copy, and returns the next_state that would result.
        This function may choose not to modify the simulation environment. It
        can be used for applications that test the outcome of an action befoe
        execution (ie. generating heatmaps).

        Parameters
        ----------
        state       : State
            Current state of the environment
        action      : Action
            Action taken from the state
        add_to_sim  : bool, optional
            Default True, flag for whether to add the newly placed object to the simulation (plotted figure)

        Returns
        -------
        next_state : State
            The state resulting from applying the action to its own next_object

        """
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
        """Executes the action on the action's next_object and returns the
        next_state that would result.

        Parameters
        ----------
        state       : State
            Current state of the environment
        action      : Action
            Action taken from the state
        add_to_sim  : bool, optional
            Default True, flag for whether to add the newly placed object to the simulation (plotted figure)

        Returns
        -------
        next_state : State
            The state resulting from applying the action to its own next_object

        """
        next_state = state.copy()
        action.next_object.apply_transform(action.transform)
        if (add_to_sim):
            add_object(self.fig, self.ax, action.next_object)
            # add_object(self.fig, self.ax, action.next_object.bounding_box())

        next_state.objects.append(action.next_object)
        # Pick a new next object
        # next_state.next_object = Square(5, np.eye(3))
        next_state.next_object = PlacementObject.get_random()#Rectangle.get_random(2, 10) #
        while (next_state.next_object.polygon.is_valid == False):
            next_state.next_object = PlacementObject.get_random() #Rectangle.get_random(2, 10) #
        return next_state

class Termination:
    """This is a representation of termination states for the bin placing project.
    A bin placing termination contains only a function done() which takes in a state
    and decides whether we are finished with the placement task.

    """

    def done(self, state):
        """Decides whether the input state is a termination state.

        Parameters
        ----------
        state       : State
            Current state of the environment

        Returns
        -------
        bool
            True if done with the placement task, False otherwise

        """
        # Go through the objects pairwise and return True if any overlap
        # Also return True if any object is outside the bin
        for objA in state.objects:
            bin_contained = intersecting(objA, state.bin)
            if (not math.isclose(bin_contained - objA.polygon.area, 0, abs_tol=0.0001)):
            # if (bin_contained < objA.polygon.area):
                print("Bin contained = " + str(bin_contained) + " < polygon area = " + str(objA.polygon.area))
                return True
            for objB in [i for i in state.objects if i != objA]:
                if (not math.isclose(intersecting(objA, objB), 0, abs_tol=0.0001)):
                # if intersecting(objA, objB) > 0:
                    print("Object " + str(np.array(objA.polygon.exterior.coords)) + " intersects " + str(np.array(objB.polygon.exterior.coords)))
                    return True
        return False

class Value:
    """This is a representation of value functions for the bin placing project.
    A bin placing value function contains only a function evaluate() which takes
    in a state and determines its value. This may be useful for Q-learning or
    value iteration in the future.

    """

    def evaluate(self, state):
        return 0
