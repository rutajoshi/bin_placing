from matplotlib import pyplot
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch
import math

SIZE = (8.0, 4.0*(math.sqrt(5)-1))

COLOR = {
    True:  '#6699cc',
    False: '#ff3333'
    }

def v_color(ob):
    return COLOR[ob.is_valid]

def plot_coords(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, 'o', color='#999999', zorder=1)

fig = pyplot.figure(1, figsize=SIZE, dpi=90)

# 1: valid polygon
ax = fig.add_subplot(121)

ext = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
int = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)][::-1]
polygon = Polygon(ext, [int])

plot_coords(ax, polygon.interiors[0])
plot_coords(ax, polygon.exterior)

patch = PolygonPatch(polygon, facecolor=v_color(polygon), edgecolor=v_color(polygon), alpha=0.5, zorder=2)
ax.add_patch(patch)

ax.set_title('a) valid')

x_range = [-1, 3]
y_range = [-1, 3]
ax.set_xlim(*x_range)
ax.set_xticks(list(range(*x_range)) + [x_range[-1]])
ax.set_ylim(*y_range)
ax.set_yticks(list(range(*y_range)) + [y_range[-1]])
ax.set_aspect(1)

#2: invalid self-touching ring
ax = fig.add_subplot(122)
ext = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
int = [(1, 0), (0, 1), (0.5, 1.5), (1.5, 0.5), (1, 0)][::-1]
polygon = Polygon(ext, [int])

plot_coords(ax, polygon.interiors[0])
plot_coords(ax, polygon.exterior)

patch = PolygonPatch(polygon, facecolor=v_color(polygon), edgecolor=v_color(polygon), alpha=0.5, zorder=2)
ax.add_patch(patch)

ax.set_title('b) invalid')

x_range = [-1, 3]
y_range = [-1, 3]
ax.set_xlim(*x_range)
ax.set_xticks(list(range(*x_range)) + [x_range[-1]])
ax.set_ylim(*y_range)
ax.set_yticks(list(range(*y_range)) + [y_range[-1]])
ax.set_aspect(1)

pyplot.show()
