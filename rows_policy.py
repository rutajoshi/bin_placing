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
        bb_rotation = np.array([[np.cos(-theta), -np.sin(-theta), 0],
                                [np.sin(-theta), np.cos(-theta), 0],
                                [0, 0, 1]])
        obj_copy = state.next_object.copy()
        obj_copy.apply_transform(bb_rotation)
        # oriented_bb.apply_transform(bb_rotation)
        aabb = obj_copy.bounding_box()

        # Translate bounding box so that it is centered at (0,0)
        avgpt = np.mean(np.array(aabb.polygon.exterior.coords), axis=0)
        move_to_center = np.array([[1, 0, -avgpt[0]],
                                   [0, 1, -avgpt[1]],
                                   [0, 0, 1]])
        aabb.apply_transform(move_to_center)
        new_avgpt = np.mean(np.array(aabb.polygon.exterior.coords), axis=0)

        best_rotation = 0
        next_row = False

        # Go through all the objects already in the bin
        place_x = left_edge
        place_y = self.next_y  # the y-value of the next row after this one
        adjacent_y = self.old_y

        # Go through objects in the current row only (see the first if statement)
        for obj in state.objects:
            points = np.array(obj.bounding_box().polygon.exterior.coords)
            # Get the bottom right corner of the polygon
            biggest_x = np.max(points, axis=0)[0]   # biggest x among the points of this object (rightmost)
            smallest_y = np.min(points, axis=0)[1]  # smallest y seen among points of this object (bottommost)
            biggest_y = np.max(points, axis=0)[1] # get the top right corner's y-value too (topmost)

            # if this object is not in the current row, continue (skip it)
            if (smallest_y < self.old_y):
                continue

            # Update place_y, which holds the max height of any object in this row
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
                    # object does not fit in this row. Start next row
                    place_x = left_edge
                    adjacent_y = self.next_y
                    self.old_y = self.next_y
                    next_row = True
                    # self.next_y = place_y
                    break # Don't continue looking through objects in this bin if you can't fit in this row
                else:
                    best_rotation = np.pi / 2


        if (best_rotation != 0 and \
            state.bin.length/2 - place_x >= aabb.width and \
            state.bin.width/2 - adjacent_y >= aabb.length):
            # There is space for the next object in this row, rotated
            transform = np.array([[np.cos(best_rotation), -1*np.sin(best_rotation), place_x + aabb.width/2],
                                  [np.sin(best_rotation), np.cos(best_rotation), adjacent_y + aabb.length/2],
                                  [0, 0, 1]])
            final_transform = np.matmul(transform, np.matmul(move_to_center, bb_rotation))
            action = Action(final_transform, state.next_object)
            return action
        elif (state.bin.length/2 - place_x >= aabb.length and \
            state.bin.width/2 - adjacent_y >= aabb.width):
            # There is space for the next object in this row, NOT rotated
            transform = np.array([[np.cos(best_rotation), -1*np.sin(best_rotation), place_x + aabb.length/2],
                                  [np.sin(best_rotation), np.cos(best_rotation), adjacent_y + aabb.width/2],
                                  [0, 0, 1]])
            final_transform = np.matmul(transform, np.matmul(move_to_center, bb_rotation))
            action = Action(final_transform, state.next_object)
            return action
        elif (next_row and \
              state.bin.length / 2 - place_x >= aabb.width and \
              state.bin.width / 2 - adjacent_y >= aabb.length):
            # The object fits in the next row if you rotate it
            transform = np.array([[np.cos(np.pi/2), -1 * np.sin(np.pi/2), place_x + aabb.width / 2],
                                  [np.sin(np.pi/2), np.cos(np.pi/2), adjacent_y + aabb.length / 2],
                                  [0, 0, 1]])
            final_transform = np.matmul(transform, np.matmul(move_to_center, bb_rotation))
            action = Action(final_transform, state.next_object)

        # When the bin is full, place object randomly
        # This means the object doesn't fit in this row in either orientation, neither does it fit in the next row in either orientation
        theta = np.random.uniform(0, 2*np.pi)
        bin_length = state.bin.length
        bin_width = state.bin.width

        transform = np.array([[np.cos(theta), -1*np.sin(theta), np.random.uniform(-bin_length/2, bin_length/2)],
                              [np.sin(theta), np.cos(theta), np.random.uniform(-bin_width/2, bin_width/2)],
                              [0, 0, 1]])
        final_transform = np.matmul(transform, np.matmul(move_to_center, bb_rotation))
        action = Action(final_transform, state.next_object)
        return action
