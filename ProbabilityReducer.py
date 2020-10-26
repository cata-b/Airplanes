from DirectionsHelper import *
from copy import deepcopy
import texttable

class ProbabilityReducer(object):
    """
    Represents an 8x8 board (1-based coords) in which each element contains a list of possible directions for a plane with the head at that place; max length of that list is 4.
    If a square is marked as a miss, from the lists of surrounding squares the impossible directions will be removed.
    """

    def __init__(self):
        self._data = {}
        data = self._data
        for i in range(3, 7):
            data[(1, i)] = [up()]
            data[(2, i)] = [up()]
            data[(i, 1)] = [left()]
            data[(i, 2)] = [left()]
            data[(i, 8)] = [right()]
            data[(i, 7)] = [right()]
            data[(8, i)] = [down()]
            data[(7, i)] = [down()]

        data[(3, 3)] = [up(), left()]
        data[(3, 6)] = [up(), right()]
        data[(6, 3)] = [down(), left()]
        data[(6, 6)] = [down(), right()]

        data[(3, 4)] = [up(), left(), right()]
        data[(3, 5)] = [up(), left(), right()]
        data[(4, 3)] = [up(), left(), down()]
        data[(5, 3)] = [up(), left(), down()]
        data[(6, 4)] = [down(), left(), right()]
        data[(6, 5)] = [down(), left(), right()]
        data[(4, 6)] = [up(), down(), right()]
        data[(5, 6)] = [up(), down(), right()]

        data[(4, 4)] = [up(), down(), left(), right()]
        data[(4, 5)] = [up(), down(), left(), right()]
        data[(5, 4)] = [up(), down(), left(), right()]
        data[(5, 5)] = [up(), down(), left(), right()]

    def __getitem__(self, coords):
        line = coords[0]
        col = coords[1]
        if not isinstance(line, int) or line < 1 or line > 8:
            raise ValueError("Invalid line key: " + str(line))
        if not isinstance(col, int) or col < 1 or col > 8:
            raise ValueError("Invalid column key: " + str(col))
        try:
            return deepcopy(self._data[(line, col)])
        except KeyError:
            return []

    def mark_square(self, coords):
        line = coords[0]
        col = coords[1]
        if not isinstance(line, int) or line < 1 or line > 8:
            raise ValueError("Invalid line key: " + line)
        if not isinstance(col, int) or col < 1 or col > 8:
            raise ValueError("Invalid column key: " + str(col))

        if coords in self._data:
            del self._data[coords]

        removal_list = [
            ([up()], [up()]),
            ([left()], [left()]),
            ([down()], [down()]),
            ([right()], [right()]),
            ([(-1, -1)], [up(), left()]),
            ([(-1, 1)], [up(), right()]),
            ([(1, -1)], [down(), left()]),
            ([(1, 1)], [down(), right()]),
            ([(-2, 0)], [up()]),
            ([(0, -2)], [left()]),
            ([(0, 2)], [right()]),
            ([(2, 0)], [down()]),
            ([(-2, -1)], [left()]),
            ([(-1, -2)], [up()]),
            ([(-2, 1)], [right()]),
            ([(-1, 2)], [up()]),
            ([(1, -2)], [down()]),
            ([(2, -1)], [left()]),
            ([(2, 1)], [right()]),
            ([(1, 2)], [down()]),
            ([(-3, -1), (-3, 0), (-3, 1)], [up()]),
            ([(-1, 3), (0, 3), (1, 3)], [right()]),
            ([(3, -1), (3, 0), (3, 1)], [down()]),
            ([(-1, -3), (0, -3), (1, -3)], [left()])]
        for removal in removal_list:
            for rel_coords in removal[0]:
                ncoords = (line + rel_coords[0], col + rel_coords[1])
                if ncoords in self._data:
                    for to_remove in removal[1]:
                        try:
                            self._data[ncoords].remove(to_remove)
                            if len(self._data[ncoords]) == 0:
                                del self._data[ncoords]
                        except KeyError:
                            pass
                        except ValueError:
                            pass

    def __str__(self):
        t = texttable.Texttable()
        t.add_row([""] + [chr(ord('A') + i) for i in range(8)])
        for i in range(1, 9):
            row = [i]
            for j in range(1, 9):
                item = self[i, j]
                res_str = ""
                for coords in item:
                    if coords == up():
                        res_str += "U"
                    elif coords == down():
                        res_str += "D"
                    elif coords == left():
                        res_str += "L"
                    elif coords == right():
                        res_str += "R"
                row.append(res_str)
            t.add_row(row)
        return t.draw()

    def get_prob_list(self, probability):
        if probability > 4 or probability < 0:
            return []
        result = []
        for coords in self._data:
            if len(self._data[coords]) == probability:
                result.append(coords)
        return result

    def get_all_list(self):
        return list(self._data.keys())