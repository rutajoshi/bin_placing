# from utils import *
from matplotlib import pyplot
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch
import math
import numpy as np

class PlacementObject:
    """
    This class is the parent class of any polygons that you can place in a bin.
    A placement object has, at minimum, a polygon, transform, and a type.
    The polygon is already transformed to be in the orientation specified by the transform from (0,0).
    """
    def __init__(self, polygon, transform=np.eye(3), type="square"):
        self.polygon = polygon
        self.points = np.array(self.polygon.exterior.coords) # original, un-transformed points
        self.transform = transform
        self.rotation = transform[:2,:2]
        self.translation = transform[:2,2]
        self.type = type
        # Apply the transform without changing the self.points
        ext = np.matmul(self.rotation, self.points.T).T
        ext += self.translation
        self.polygon = Polygon(ext)

    def get_polygon(self):
        return self.polygon

    def get_type(self):
        return type

    def get_transform(self):
        return self.transform

    def set_transform(self, transform):
        # Only use this if you want to set the transform but NOT apply it.
        # Called by apply_transform to update stored transform to the one just applied.
        self.transform = transform
        self.rotation = transform[:2,:2]
        self.translation = transform[:2,2]

    def apply_transform(self, transform):
        # This lets you apply a new transform to the polygon
        rotation = transform[:2,:2]
        translation = transform[:2,2]
        # Retrieve the currently transformed points and apply transform to them
        points = np.array(self.polygon.exterior.coords)
        points = np.matmul(rotation, points.T).T
        points += translation
        self.polygon = Polygon(points)
        # Remember to update the stored transform. DO NOT update self.points
        new_transform = np.matmul(transform, self.transform)
        self.set_transform(new_transform)

    def bounding_box(self):
        points = np.array(self.polygon.exterior.coords)
        biggest_x = np.max(points, axis=0)[0]   # biggest x among the points of this object
        biggest_y = np.max(points, axis=0)[1]   # biggest x among the points of this object
        smallest_x = np.min(points, axis=0)[0]  # smallest y seen among points of this object
        smallest_y = np.min(points, axis=0)[1]  # smallest y seen among points of this object
        length = biggest_x - smallest_x
        width = biggest_y - smallest_y
        bounds = [(smallest_x, smallest_y),(smallest_x, biggest_y),(biggest_x, biggest_y),(biggest_x, smallest_y)]
        poly = Polygon(bounds)
        obj = PlacementObject(poly)
        obj.length = length
        obj.width = width
        return obj

class Square(PlacementObject):
    def __init__(self, side_length, transform):
        self.side_length = side_length
        self.length = side_length
        self.width = side_length
        bottom_left = (-side_length/2, -side_length/2)
        top_left = (-side_length/2, side_length/2)
        top_right = (side_length/2, side_length/2)
        bottom_right = (side_length/2, -side_length/2)
        ext = np.array([bottom_left, top_left, top_right, bottom_right, bottom_left])

        polygon = Polygon(ext)
        super(Square, self).__init__(polygon, transform, "square")

    @staticmethod
    def get_random(min_side_length, max_side_length):
        # Generates a random square with min and max side lengths specified
        # Make it not and not translated from (0,0)
        s = np.random.randint(min_side_length, max_side_length)
        # theta = np.random.uniform(0, 2*np.pi)
        # transform = np.array([[np.cos(theta), -np.sin(theta), 0],
        #                       [np.sin(theta), np.cos(theta), 0],
        #                       [0, 0, 1]])
        return Square(s, np.eye(3))

class Rectangle(PlacementObject):
    def __init__(self, length, width, transform):
        self.length = length
        self.width = width
        bottom_left = (-length/2, -width/2)
        top_left = (-length/2, width/2)
        top_right = (length/2, width/2)
        bottom_right = (length/2, -width/2)
        ext = [bottom_left, top_left, top_right, bottom_right, bottom_left]

        polygon = Polygon(ext)
        super(Rectangle, self).__init__(polygon, transform, "rectangle")

    @staticmethod
    def get_random(min_side_length, max_side_length):
        # Generates a random rectange with min and max side lengths specified
        # Make it randomly rotated but not translated from (0,0)
        l = np.random.randint(min_side_length, max_side_length)
        w = np.random.randint(min_side_length, max_side_length)
        # theta = np.random.uniform(0, 2*np.pi)
        # transform = np.array([[np.cos(theta), -np.sin(theta), 0],
        #                       [np.sin(theta), np.cos(theta), 0],
        #                       [0, 0, 1]])
        return Rectangle(l, w, np.eye(3))

class AbstractShape(PlacementObject):
    def __init__(self, points, transform):
        polygon = Polygon(points)
        super(AbstractShape, self).__init__(polygon, transform, "abstract")
