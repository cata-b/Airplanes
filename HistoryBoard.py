import texttable
class HistoryBoard(object):
    """
    Represents an 8x8 board for keeping track of hits, misses, and destroyed planes
    """
    def __init__(self):
        self._data = {}

    def copy_from_airplane_board(self, board):
        for coords in board._occupied:
            self.mark_plane(coords)

    def mark_hit(self, coords):
        line = coords[0]
        col = coords[1]
        if not isinstance(line, int) or line < 1 or line > 8:
            raise ValueError("Invalid line key: " + line)
        if not isinstance(col, int) or col < 1 or col > 8:
            raise ValueError("Invalid column key: " + col)
        self._data[coords] = 'H'

    def mark_miss(self, coords):
        line = coords[0]
        col = coords[1]
        if not isinstance(line, int) or line < 1 or line > 8:
            raise ValueError("Invalid line key: " + line)
        if not isinstance(col, int) or col < 1 or col > 8:
            raise ValueError("Invalid column key: " + col)
        self._data[coords] = 'M'
    
    def mark_plane(self, coords):
        line = coords[0]
        col = coords[1]
        if not isinstance(line, int) or line < 1 or line > 8:
            raise ValueError("Invalid line key: " + line)
        if not isinstance(col, int) or col < 1 or col > 8:
            raise ValueError("Invalid column key: " + col)
        self._data[coords] = 'P'

    def __getitem__(self, coords):
        line = coords[0]
        col = coords[1]
        if not isinstance(line, int) or line < 1 or line > 8:
            raise ValueError("Invalid line key: " + str(line))
        if not isinstance(col, int) or col < 1 or col > 8:
            raise ValueError("Invalid column key: " + str(col))
        try:
            return self._data[coords]
        except KeyError:
            return ""

    def __str__(self):
        t = texttable.Texttable()
        t.add_row([""] + [chr(ord('A') + i) for i in range(8)])
        for i in range(1, 9):
            row = [i]
            for j in range(1, 9):
                row.append(self[i, j])
            t.add_row(row)
        return t.draw()