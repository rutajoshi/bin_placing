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

        # Go through all the objects already in the bin
        place_x = left_edge
        adjacent_y = self.old_y

        for obj in state.objects:
            points = np.array(obj.polygon.exterior.coords)
            biggest_x = np.max(points, axis=0)[0]   # biggest x among the points of this object
            smallest_y = np.min(points, axis=0)[1]  # smallest y seen among points of this object
            biggest_y = np.max(points, axis=0)[1]

            # if this object is not in the current row, continue (skip it)
            if (smallest_y < self.old_y):
                continue

            # find the y value of the lowest point with biggest x in this object (bottom right corner)
            a = [list(i) for i in points if i[0] == biggest_x]
            right_bottom = np.min(a, axis=0)[1]
            # If this object is further right than objects seen so far, set the adjacent_y to be this object's bottom right edge
            if (biggest_x > place_x):
                place_x = biggest_x   # biggest x seen so far in this row
                adjacent_y = right_bottom
                self.next_y = biggest_y

            # If there is no space in this row, because this object is too far to the right, then set stuff appropriately and break
            if (state.bin.length/2 - place_x < state.next_object.length):
                place_x = left_edge
                adjacent_y = self.next_y
                self.old_y = self.next_y
                self.next_y = biggest_y
                break

        print("place_x = " + str(place_x))
        print("adjacent_y = " + str(adjacent_y))

        if (state.bin.length/2 - place_x >= state.next_object.length and \
            state.bin.width/2 - adjacent_y >= state.next_object.width):
            # There is space for the next object in this row
            transform = np.array([[1, 0, place_x + state.next_object.length/2],
                                  [0, 1, adjacent_y + state.next_object.width/2],
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
