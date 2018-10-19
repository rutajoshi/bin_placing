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
    index = np.random.choice(len(COLOR))
    return COLOR[index]

def plot_coords(ax, ob, color):
    x, y = ob.xy
    ax.plot(x, y, 'o', color=color, zorder=1)

def create_env():
    # Create the figure for matplotlib to which you will add the objects
    fig = pyplot.figure(1, figsize=SIZE, dpi=90)
    return fig

def add_bin(fig, length, width):
    # Code to create a bin and to add it to the figure
    ax = fig.add_subplot(121)
    bin = Rectangle(length, width, np.eye(3))
    polygon = bin.polygon
    # bottom_left = (-length/2, -width/2)
    # top_left = (-length/2, width/2)
    # top_right = (length/2, width/2)
    # bottom_right = (length/2, -width/2)
    # ext = [bottom_left, top_left, top_right, bottom_right, bottom_left]
    # polygon = Polygon(ext)

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
    polygon = object.polygon
    color = v_color(polygon)

    plot_coords(ax, polygon.exterior, color)

    patch = PolygonPatch(polygon, facecolor=color, edgecolor=color, alpha=0.5, zorder=2)
    ax.add_patch(patch)
    return None

def intersecting(objA, objB):
    # If objA and objB intersect, returns the area of the intersection
    # Otherwise returns 0
    p1 = objA.polygon
    p2 = objB.polygon
    p3 = p1.intersection(p2)
    return p3.area

def display_env():
    # May be unnecessary
    pyplot.show()
