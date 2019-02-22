from mdp import *

class RowsPolicy(Policy):
    def __init__(self, bin_length, bin_width):
        super(RowsPolicy, self).__init__(bin_width, bin_length)
        self.next_y = -self.bin_width / 2
        self.old_y = -self.bin_width / 2

    def get_action(self, state):
        # Get the bin
        left_edge = -self.bin_length / 2
        bottom_edge = -self.bin_width / 2

        # Get the oriented bounding box of the next object
        # aabb = state.next_object.bounding_box()
        oriented_bb = state.next_object.oriented_bounding_box()

        # Axis align the bounding box
        bb_points = np.array(oriented_bb.polygon.exterior.coords)
        side = bb_points[1] - bb_points[0]
        y_axis = np.array([0, 1])
        theta = np.arccos((np.dot(side, y_axis)) / (np.linalg.norm(side) * np.linalg.norm(y_axis)))
        bb_rotation = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta), np.cos(theta), 0],
                                [0, 0, 1]])
        oriented_bb.apply_transform(bb_rotation)
        aabb = oriented_bb.bounding_box()


        best_rotation = 0

        # Go through all the objects already in the bin
        place_x = left_edge
        place_y = self.next_y  # the y-value of the next row after this one
        adjacent_y = self.old_y

        # Go through objects in the current row only (see the first if statement)
        for obj in state.objects:
            points = np.array(obj.bounding_box().polygon.exterior.coords)
            # Get the bottom right corner of the polygon
            biggest_x = np.max(points, axis=0)[0]   # biggest x among the points of this object
            smallest_y = np.min(points, axis=0)[1]  # smallest y seen among points of this object
            biggest_y = np.max(points, axis=0)[1] # get the top right corner's y-value too

            # if this object is not in the current row, continue (skip it)
            if (smallest_y < self.old_y):
                continue

            # Update place_y, which holds the height of this row
            if (biggest_y > place_y):
                place_y = biggest_y

            # find the y value of the lowest point with biggest x in this object (bottom right corner)
            a = [list(i) for i in points if i[0] == biggest_x]
            right_bottom = np.min(a, axis=0)[1]
            # If this object is further right than objects seen so far, set the adjacent_y to be this object's bottom right edge
            if (biggest_x > place_x):
                place_x = biggest_x   # biggest x seen so far in this row
                adjacent_y = right_bottom
                self.next_y = place_y

            # Check if the aabb fits in its current rotation
            # If it does not, check if it fits with a 90 degree rotation
            # Otherwise there is no space in the row, so set stuff to the next row
            if (state.bin.length/2 - place_x < aabb.length):
                if (state.bin.length/2 - place_x < aabb.width):
                    place_x = left_edge
                    adjacent_y = self.next_y
                    self.old_y = self.next_y
                    self.next_y = place_y
                    break
                else:
                    best_rotation = np.pi / 2

        # print("place_x = " + str(place_x))
        # print("adjacent_y = " + str(adjacent_y))

        left_wiggle_room = 0
        if (place_x == left_edge):
            left_wiggle_room = 0.1
        bottom_wiggle_room = 0
        if (adjacent_y == bottom_edge):
            bottom_wiggle_room = 0.1

        if (best_rotation != 0 and \
            state.bin.length/2 - place_x >= aabb.width and \
            state.bin.width/2 - adjacent_y >= aabb.length):
            # rotation = np.array([[np.cos(best_rotation), -1*np.sin(best_rotation)],
            #                      [np.sin(best_rotation), np.cos(best_rotation)]])
            # result = np.matmul(bb_rotation[:2,:2], rotation)
            # transform = np.array([[result[0,0], result[0,1], place_x + aabb.width/2],
            #                       [result[1,0], result[1,1], adjacent_y + aabb.length/2],
            #                       [0, 0, 1]])

            transform = np.array([[np.cos(best_rotation), -1*np.sin(best_rotation), place_x + aabb.width/2 + left_wiggle_room],
                                  [np.sin(best_rotation), np.cos(best_rotation), adjacent_y + aabb.length/2 + bottom_wiggle_room],
                                  [0, 0, 1]])
            action = Action(transform, state.next_object)
            return action
        elif (state.bin.length/2 - place_x >= aabb.length and \
            state.bin.width/2 - adjacent_y >= aabb.width):
            # There is space for the next object in this row
            # rotation = np.array([[np.cos(best_rotation), -1 * np.sin(best_rotation)],
            #                      [np.sin(best_rotation), np.cos(best_rotation)]])
            # result = np.matmul(bb_rotation[:2, :2], rotation)
            # transform = np.array([[result[0, 0], result[0, 1], place_x + aabb.length/2],
            #                       [result[1, 0], result[1, 1], adjacent_y + aabb.width/2],
            #                       [0, 0, 1]])
            transform = np.array([[np.cos(best_rotation), -1*np.sin(best_rotation), place_x + aabb.length/2 + left_wiggle_room],
                                  [np.sin(best_rotation), np.cos(best_rotation), adjacent_y + aabb.width/2 + bottom_wiggle_room],
                                  [0, 0, 1]])
            action = Action(transform, state.next_object)
            return action

        # When the bin is full, place object randomly
        theta = np.random.uniform(0, 2*np.pi)
        bin_length = state.bin.length
        bin_width = state.bin.width

        transform = np.array([[np.cos(theta), -1*np.sin(theta), np.random.uniform(-bin_length/2, bin_length/2)],
                              [np.sin(theta), np.cos(theta), np.random.uniform(-bin_width/2, bin_width/2)],
                              [0, 0, 1]])
        action = Action(transform, state.next_object)
        return action
