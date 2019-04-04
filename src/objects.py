# from utils import *
from matplotlib import pyplot
from shapely.geometry import Polygon
from shapely.geometry import Point
from descartes.patch import PolygonPatch
import math
import random
import numpy as np


class BagOfPoints:
    """This class is a representation of a list of points that together may form
    a PlacementObject.
    """

    def __init__(self, list_of_points):
        """Initializes a BagOfPoints, given a list of points.

        Parameters
        ----------
        list_of_points  : list
            A list of 2D coordinates for points defining this object

        Returns
        -------
        BagOfPoints
            An instance of BagOfPoints with the above parameters

        """
        self.list_of_points = list(list_of_points)

    @staticmethod
    def generate_random(number, bound):
        """Generates a random BagOfPoints given a number of points and a size length
        for a bounding square within which to generate the points.

        Parameters
        ----------
        number   : int
            Number of points
        bound   : int
            Side length for a bounding square within which to generate points

        Returns
        -------
        BagOfPoints
            A BagOfPoints with `number` points within a square of side length `bound`

        """
        list_of_pts = []
        bounding_square = Square(bound, np.eye(3))
        minx, miny = -bound, -bound
        maxx, maxy = bound, bound
        counter = 0
        while counter < number:
            pnt = (np.random.randint(minx, maxx), np.random.randint(miny, maxy))
            if bounding_square.get_polygon().contains(Point(pnt)):
                list_of_pts.append(pnt)
                counter += 1
        list_of_pts.append(list_of_pts[0])
        return BagOfPoints(list_of_pts)


class PlacementObject:
    """This class is the parent class of any polygons that you can place in a bin.
    A placement object has, at minimum, a polygon, transform, and a type.
    The polygon is already transformed to be in the orientation specified by the
    transform from origin (0,0) in world space coordinates.
    """

    def __init__(self, polygon, transform=np.eye(3), type="square"):
        """Initializes a PlacementObject, given a list of points.

        Parameters
        ----------
        polygon     : shapely.Polygon
            A shapely module polygon
        transform   : numpy array
            A 3x3 homogeneous coordinates transformation matrix, identity by default
        type        : str
            The type of polygon, "square" by default

        Returns
        -------
        PlacementObject
            An instance of PlacementObject with the above parameters

        """
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
        """Getter method for this PlacementObject's polygon.

        Returns
        -------
        polygon : shapely.Polygon
            The shapely Polygon associated with this PlacementObject

        """
        return self.polygon

    def get_type(self):
        """Getter method for this PlacementObject's type.

        Returns
        -------
        typestring : str
            The string type associated with this PlacementObject

        """
        return type

    def get_transform(self):
        """Getter method for this PlacementObject's transform.

        Returns
        -------
        transform : numpy array
            The 3x3 homogeneous transform of this PlacementObject.

        """
        return self.transform

    def set_transform(self, transform):
        """Setter method for this PlacementObject's tranform.  Only use this if
        you want to set the transform but NOT apply it. Called by apply_transform
        to update stored transform to the one just applied.
        """
        self.transform = transform
        self.rotation = transform[:2,:2]
        self.translation = transform[:2,2]

    def apply_transform(self, transform):
        """Applies the input transform to the polygon:
        1) Retrieves the currently transformed points of this polygon
        2) Apply the transform to those points
        3) Generate a new shapely Polygon with those points
        4) Reset self.polygon and call set_transform to update self's transform parameters
        5) DO NOT update self.points (these should remain the untransformed points of the original polygon)

        Parameters
        ----------
        transform   : numpy array
            A 3x3 homogeneous coordinates transformation matrix

        """
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
        """Returns the axis aligned bounding box of this PlacementObject.

        Returns
        -------
        PlacementObject
            A PlacementObject which contains a polygon representing the axis
            aligned bounding box of self's polygon.

        """
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

    def oriented_bounding_box(self):
        """Returns the non-aligned, oriented bounding box of this PlacementObject.

        Returns
        -------
        PlacementObject
            A PlacementObject which contains a polygon representing the oriented
            bounding box of self's polygon. This is the minimum rotated rectangle.

        """
        rect_box_tilted = self.polygon.minimum_rotated_rectangle
        obj = PlacementObject(rect_box_tilted)
        return obj

    def copy(self):
        """Returns a shallow copy of this PlacementObject.

        Returns
        -------
        PlacementObject
            An instance of PlacementObject with the same parameters as self.

        """
        return PlacementObject(self.polygon, self.transform, self.type)

    @staticmethod
    def get_random():
        """Returns a random PlacementObject generated from a random BagOfPoints.

        Returns
        -------
        PlacementObject
            An instance of PlacementObject generated with 3-8 vertices, bounded by a 2-10 side length square

        """
        number_of_vertices = np.random.randint(3, 8)
        size_bound = np.random.randint(2, 10)
        bop = BagOfPoints.generate_random(number_of_vertices, size_bound)
        print("Random polygon has points = " + str(bop.list_of_points) + "\n")
        # Get the minimum area bounding box for this object and return it
        # shape = AbstractShape(bop.list_of_points, np.eye(3))
        base_polygon = Polygon(bop.list_of_points)
        return PlacementObject(base_polygon, np.eye(3), "random")


class Square(PlacementObject):
    """This is a representation of a square shaped PlacementObject.
    """

    def __init__(self, side_length, transform):
        """Initializes a Square, given a side length and transform.

        Parameters
        ----------
        side_length : int
            Side length of a square
        transform   : numpy array
            A 3x3 homogeneous coordinates transformation matrix

        Returns
        -------
        Square
            An instance of Square with the above parameters

        """
        self.side_length = side_length
        self.length = side_length
        self.width = side_length
        self.area = side_length**2
        bottom_left = (-side_length/2, -side_length/2)
        top_left = (-side_length/2, side_length/2)
        top_right = (side_length/2, side_length/2)
        bottom_right = (side_length/2, -side_length/2)
        ext = np.array([bottom_left, top_left, top_right, bottom_right, bottom_left])

        polygon = Polygon(ext)
        super(Square, self).__init__(polygon, transform, "square")

    @staticmethod
    def get_random(min_side_length, max_side_length):
        """Returns a random Square object with side length between the passed in
        minimum and maximum.

        Parameters
        ----------
        min_side_length : int
            Minimum side length of random square
        max_side_length : int
            Maximum side length of random square

        Returns
        -------
        Square
            A random instance of Square with side length between the above
            parameters, at the origin in world space.

        """
        # Generates a random square with min and max side lengths specified
        # Make it not and not translated from (0,0)
        s = np.random.randint(min_side_length, max_side_length)
        # theta = np.random.uniform(0, 2*np.pi)
        # transform = np.array([[np.cos(theta), -np.sin(theta), 0],
        #                       [np.sin(theta), np.cos(theta), 0],
        #                       [0, 0, 1]])
        return Square(s, np.eye(3))

class Rectangle(PlacementObject):
    """This is a representation of a rectangle shaped PlacementObject.
    """

    def __init__(self, length, width, transform):
        """Initializes a Rectangle, given a length, width, and transform.

        Parameters
        ----------
        length : int
            Length of a rectangle (x)
        width  : int
            Width of a rectangle (y)
        transform   : numpy array
            A 3x3 homogeneous coordinates transformation matrix

        Returns
        -------
        Rectangle
            An instance of Rectangle with the above parameters

        """
        self.length = length
        self.width = width
        self.area = length * width
        self.transform = transform
        bottom_left = (-length/2, -width/2)
        top_left = (-length/2, width/2)
        top_right = (length/2, width/2)
        bottom_right = (length/2, -width/2)
        ext = [bottom_left, top_left, top_right, bottom_right, bottom_left]

        polygon = Polygon(ext)
        super(Rectangle, self).__init__(polygon, transform, "rectangle")

    @staticmethod
    def get_random(min_side_length, max_side_length):
        """Returns a random Rectangle object with length and width between the
        passed in minimum and maximum side lengths.

        Parameters
        ----------
        min_side_length : int
            Minimum side length (or width) of a random rectangle
        max_side_length : int
            Maximum side length (or width) of a random rectangle

        Returns
        -------
        Rectangle
            A random instance of Rectangle with side length and width between
            the above parameters, at the origin in world space.

        """
        # Generates a random rectangle with min and max side lengths specified
        # Make it randomly rotated but not translated from (0,0)
        l = np.random.randint(min_side_length, max_side_length)
        w = np.random.randint(min_side_length, max_side_length)
        # theta = np.random.uniform(0, 2*np.pi)
        # transform = np.array([[np.cos(theta), -np.sin(theta), 0],
        #                       [np.sin(theta), np.cos(theta), 0],
        #                       [0, 0, 1]])
        return Rectangle(l, w, np.eye(3))

    def copy(self):
        """Returns a shallow copy of this rectangle.

        Returns
        -------
        Rectangle
            An instance of Rectangle with the same parameters as self.

        """
        return Rectangle(self.length, self.width, self.transform)

class AbstractShape(PlacementObject):
    """This is a representation of an abstractly shaped PlacementObject.
    """

    def __init__(self, points, transform):
        """Initializes a Rectangle, given a polygon and transform.

        Parameters
        ----------
        polygon : shapely.Polygon
            An arbitrary shapely polygon
        transform   : numpy array
            A 3x3 homogeneous coordinates transformation matrix

        Returns
        -------
        AbstractShape
            An instance of AbstractShape with the above parameters

        """
        polygon = Polygon(points)
        super(AbstractShape, self).__init__(polygon, transform, "abstract")
