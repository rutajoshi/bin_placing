from objects import *

ENV_CREATED = False

SIZE = (8.0, 4.0*(math.sqrt(5)-1))
COLOR = {
    0: '#32fffb',   #blue
    1: '#ff3333',   #red
    2: '#6fff31',   #green
    3: '#9830ff',   #purple
    4: '#fff130'    #yellow
    }

def v_color(ob):
    """Returns a random hex color code by sampling from a finite set.

    Parameters
    ----------
    ob       : PlacementObject
        A placement object to color.

    Returns
    -------
    str
        The hex color code of one of 5 colors

    """
    index = np.random.choice(len(COLOR))
    return COLOR[index]

def plot_coords(ax, ob, color):
    """Plots an object's xy coordinates on the figure of the bin, given axes and
    color.

    Parameters
    ----------
    ax  : an matplotlib.axes.SubplotBase subclass of Axes (or a subclass of Axes)
        The axes of the subplot corresponding to the bin
    ob  : PlacementObject
        Object to be displayed in the matplotlib simulation
    color  : str
        The hex color code of one of 5 colors

    """
    x, y = ob.xy
    ax.plot(x, y, 'o', color=color, zorder=1)

def create_env():
    """Creates the figure for matplotlib to which you will add the objects.

    Returns
    -------
    fig : matplotlib.pyplot.Figure
        Figure used to display the bin and objects

    """
    # Create the figure for matplotlib to which you will add the objects
    fig = pyplot.figure(1, figsize=SIZE, dpi=90)
    return fig

def add_bin(fig, length, width):
    """Creates the bin object given dimensions and a figure.

    Parameters
    ----------
    fig : matplotlib.pyplot.Figure
        Figure used to display the bin and objects
    length : int
        Length of a rectangle (x) used for creating the bin
    width  : int
        Width of a rectangle (y) used for creating the bin

    Returns
    -------
    ax  : an matplotlib.axes.SubplotBase subclass of Axes (or a subclass of Axes)
        The axes of the subplot corresponding to the bin
    bin : the Rectangle object corresponding to the bin

    """
    # Code to create a bin and to add it to the figure
    ax = fig.add_subplot(121)
    bin = Rectangle(length, width, np.eye(3))
    polygon = bin.polygon

    plot_coords(ax, polygon.exterior, '#999999')

    patch = PolygonPatch(polygon, facecolor='#999999', edgecolor='#999999', alpha=0.5, zorder=2)
    ax.add_patch(patch)

    ax.set_title('bin')

    x_range = [-length, length]
    y_range = [-width, width]
    ax.set_xlim(*x_range)
    ax.set_xticks(list(range(*x_range)) + [x_range[-1]])
    ax.set_ylim(*y_range)
    ax.set_yticks(list(range(*y_range)) + [y_range[-1]])
    ax.set_aspect(1)
    return ax, bin

def add_object(fig, ax, object):
    """Adds an input object to the matplotlib simulation given the figure and
    axes for the bin.

    Parameters
    ----------
    fig : matplotlib.pyplot.Figure
        Figure used to display the bin and objects
    ax  : an matplotlib.axes.SubplotBase subclass of Axes (or a subclass of Axes)
        The axes of the subplot corresponding to the bin
    object  : PlacementObject
        Object to be added to the bin

    """
    polygon = object.polygon
    color = v_color(polygon)

    plot_coords(ax, polygon.exterior, color)

    patch = PolygonPatch(polygon, facecolor=color, edgecolor=color, alpha=0.5, zorder=2)
    ax.add_patch(patch)
    return None

def intersecting(objA, objB):
    """Checks whether input placement objects objA and objB intersect.

    Parameters
    ----------
    objA : PlacementObject
        First object
    objB : PlacementObject
        Second object

    Returns
    -------
    float
        The 2D area overlap of objA and objB

    """
    # If objA and objB intersect, returns the area of the intersection
    # Otherwise returns 0
    p1 = objA.polygon
    p2 = objB.polygon
    p3 = p1.intersection(p2)
    # import pdb;pdb.set_trace();
    return p3.area

def display_env():
    """Displays the matplotlib simulation by calling pyplot.show().
    """
    # May be unnecessary
    pyplot.show()
