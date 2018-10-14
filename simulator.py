# 2d simulator that will drop polygons into a bounded rectangle

from matplotlib import pyplot
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch
import math
import numpy as np


#### UTILS ####

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


#### The actual code ####

def create_env():
    # Create the figure for matplotlib to which you will add the objects
    fig = pyplot.figure(1, figsize=SIZE, dpi=90)
    return fig

def add_bin(fig, length, width):
    # Code to create a bin and to add it to the figure
    ax = fig.add_subplot(121)
    bottom_left = (-length/2, -width/2)
    top_left = (-length/2, width/2)
    top_right = (length/2, width/2)
    bottom_right = (length/2, -width/2)
    ext = [bottom_left, top_left, top_right, bottom_right, bottom_left]
    polygon = Polygon(ext)

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

    return ax

def add_square(fig, transform, side_length, ax):
    # Take the input transform (3x3) and put a fixed size square in that spot
    # Translation is from (0,0), and all transforms are applied to the center of the square
    bottom_left = (-side_length/2, -side_length/2)
    top_left = (-side_length/2, side_length/2)
    top_right = (side_length/2, side_length/2)
    bottom_right = (side_length/2, -side_length/2)
    ext = np.array([bottom_left, top_left, top_right, bottom_right, bottom_left])

    # Apply the transform rotation
    print("Transform = " + str(transform) + "\n")
    rotation = transform[:2,:2]
    translation = transform[:2,2]

    print("Original = ")
    print(ext)
    print("\n")

    ext = np.matmul(rotation, ext.T).T
    print("Rotated = ")
    print(ext)
    print("\n")

    ext += translation
    print("Translation = " + str(translation))
    print("Translated = ")
    print(ext)
    print("\n")

    polygon = Polygon(ext)
    color = v_color(polygon)

    plot_coords(ax, polygon.exterior, color)

    patch = PolygonPatch(polygon, facecolor=color, edgecolor=color, alpha=0.5, zorder=2)
    ax.add_patch(patch)
    return None

# Load the figure with just a bin, then with a bin and a square
def main():
    fig = create_env()
    ax = add_bin(fig, 20, 20)

    # Generate a random transform matrix and add square
    theta = np.random.uniform(0, 2*np.pi)
    translation = (np.random.uniform(-10, 10), np.random.uniform(-10, 10))
    transform = np.array([[np.cos(theta), -1*np.sin(theta), translation[0]],
                            [np.sin(theta), np.cos(theta), translation[1]],
                            [0,0,0]])
    # add_square(fig, np.array([[1,0,0],[0,1,0],[0,0,0]]), 5, ax)
    add_square(fig, transform, 5, ax)
    pyplot.show()

if __name__ == "__main__": main()
