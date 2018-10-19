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

    def get_polygon(self, polygon):
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

class Square(PlacementObject):
    def __init__(self, side_length, transform):
        self.side_length = side_length
        bottom_left = (-side_length/2, -side_length/2)
        top_left = (-side_length/2, side_length/2)
        top_right = (side_length/2, side_length/2)
        bottom_right = (side_length/2, -side_length/2)
        ext = np.array([bottom_left, top_left, top_right, bottom_right, bottom_left])

        polygon = Polygon(ext)
        super(Square, self).__init__(polygon, transform, "square")

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

class AbstractShape(PlacementObject):
    def __init__(self, points, transform):
        polygon = Polygon(points)
        super(AbstractShape, self).__init__(polygon, transform, "abstract")
