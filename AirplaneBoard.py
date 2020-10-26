import texttable
from DirectionsHelper import *

class AirplaneBoard(object):
    """
    Memory representation for an 8x8 board for the Airplanes game.
    Supports placing 2 planes, that don't overlap, and indexing in order to determine a hit, miss or kill
    """


    def __init__(self):
        self._occupied = [] # all occupied squares
        self._bodies = [] # lists of indices of plane body parts
        self._heads = [] # indices of plane heads


    def __getitem__(self, coords):
        """
        Returns a number corresponding to the state of a square.
        parameters: - coords: tuple of ints representing the 1-based coordinates of the square
        returns: 0 - nothing, 1 - body, 2 - head
        exceptions:
            - ValueError if coords are not int or out of [1, 8]
        """
        line = coords[0]
        col = coords[1]
        if not isinstance(line, int) or line < 1 or line > 8:
            raise ValueError("Invalid line key: " + str(line))
        if not isinstance(col, int) or col < 1 or col > 8:
            raise ValueError("Invalid column key: " + str(col))
        index = None
        try:
            index = self._occupied.index(coords)
        except ValueError:
            return 0
        if index in self._heads:
            return 2
        return 1


    def get_plane(self, head):
        """
        Returns all the parts that make a plane already placed on the board.
        parameters: head: tuple of ints, the 1-based coordinates of the head of the plane
        returns: list of tuples
        exceptions:
            ValueError if a plane head is not at the given coordinates
        """
        headlist = [self._occupied[i] for i in self._heads]
        if head not in headlist:
            raise ValueError("Head does not exist at that location.")
        index = headlist.index(head)
        result = []
        for id in self._bodies[index]:
            result.append(self._occupied[id])
        return result

    def make_body(self, head, direction):
        """
        Makes a plane body.
        parameters:
            - head: tuple of ints, the 1-based coordinates of the head of the plane
            - direction: orientation of the plane; (-1, 0) for up, (0, -1) for left, (1, 0) for down, (0, 1) for right
        exceptions:
            - ValueError if direction is not one of (-1, 0), (0, -1), (1, 0), (0, 1)
            - ValueError if plane's body/head is out of bounds
        """
        if direction not in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            raise ValueError("Invalid direction.")
        if head[0] < 1 or head[0] > 8 or head[1] < 1 or head[1] > 8:
            raise ValueError("Head is out of bounds.")
        if direction == right():
            if head[0] < 3 or head[1] < 4 or head[0] > 6:
                raise ValueError("Plane is out of bounds.")
            return \
            [(head[0] - 2, head[1] - 1), \
             (head[0] - 1, head[1] - 1), \
             (head[0],     head[1] - 1), \
             (head[0] + 1, head[1] - 1), \
             (head[0] + 2, head[1] - 1), \
             (head[0],     head[1] - 2), \
             (head[0] - 1, head[1] - 3), \
             (head[0],     head[1] - 3), \
             (head[0] + 1, head[1] - 3)  ]

        elif direction == down():
            if head[1] < 3 or head[0] < 4 or head[1] > 6:
                raise ValueError("Plane is out of bounds.")
            return \
            [(head[0] - 1, head[1] - 2), \
             (head[0] - 1, head[1] - 1), \
             (head[0] - 1, head[1]    ), \
             (head[0] - 1, head[1] + 1), \
             (head[0] - 1, head[1] + 2), \
             (head[0] - 2, head[1]    ), \
             (head[0] - 3, head[1] - 1), \
             (head[0] - 3, head[1]    ), \
             (head[0] - 3, head[1] + 1)  ]

        elif direction == left():
            if head[0] < 3 or head[1] > 5 or head[0] > 6:
                raise ValueError("Plane is out of bounds.")
            return \
            [(head[0] - 2, head[1] + 1), \
             (head[0] - 1, head[1] + 1), \
             (head[0],     head[1] + 1), \
             (head[0] + 1, head[1] + 1), \
             (head[0] + 2, head[1] + 1), \
             (head[0],     head[1] + 2), \
             (head[0] - 1, head[1] + 3), \
             (head[0],     head[1] + 3), \
             (head[0] + 1, head[1] + 3)  ]

        else: # up
            if head[1] < 3 or head[0] > 5 or head[1] > 6:
                raise ValueError("Plane is out of bounds.")
            return \
            [(head[0] + 1, head[1] - 2), \
             (head[0] + 1, head[1] - 1), \
             (head[0] + 1, head[1]    ), \
             (head[0] + 1, head[1] + 1), \
             (head[0] + 1, head[1] + 2), \
             (head[0] + 2, head[1]    ), \
             (head[0] + 3, head[1] - 1), \
             (head[0] + 3, head[1]    ), \
             (head[0] + 3, head[1] + 1)  ]

    def body_ok(self, head, body):
        """
        Checks if a plane intersects with any other already placed plane
        parameters:
            - head: tuple of ints, 1-based coordinates of the head of the plane
            - body: list of such tuples
        """
        if head in self._occupied:
            return False
        for part in body:
            if part in self._occupied:
                return False
        return True

    def place_plane(self, head, direction):
        """
        Places a plane on the board.
        parameters:
            - head: tuple of ints, the 1-based coordinates of the head of the plane
            - direction: orientation of the plane; (-1, 0) for up, (0, -1) for left, (1, 0) for down, (0, 1) for right
        returns None
        exceptions:
            - PermissionError if adding a third plane or overlapping planes.
        """
        if len(self._heads) == 2:
            raise PermissionError("Adding more than 2 planes not allowed.")
        
        plane_body = self.make_body(head, direction)
        if not self.body_ok(head, plane_body):
            raise PermissionError("Cannot overlap planes " + str(head))

        body_idx = []
        for body_part in plane_body:
            body_idx.append(len(self._occupied))
            self._occupied.append(body_part)
        self._bodies.append(body_idx)
        self._heads.append(len(self._occupied))
        self._occupied.append(head)
        return plane_body

    def __str__(self):
        t = texttable.Texttable()
        t.add_row([""] + [chr(ord('A') + i) for i in range(8)])
        for i in range(1, 9):
            row = [i]
            for j in range(1, 9):
                sq = self[i, j]
                if sq == 0:
                    row.append("")
                elif sq == 1:
                    row.append("#")
                else:
                    row.append("@")
            t.add_row(row)
        return t.draw()
