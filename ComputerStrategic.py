from ProbabilityReducer import ProbabilityReducer
from AirplaneBoard import AirplaneBoard
import random as rnd
from DirectionsHelper import *

class ComputerStrategic(object):

    def __init__(self):
        self._prob_reducer = ProbabilityReducer()
        self._board = AirplaneBoard()
        self._hits = []
        self._misses = []

    def get_plane(self, head):
        return self._board.get_plane(head)

    def place_planes(self):
        self.planes_table = ProbabilityReducer()
        first_head = rnd.choice(self.planes_table.get_all_list())
        first_orientation = rnd.choice(self.planes_table[first_head])
        first_body = self._board.place_plane(first_head, first_orientation)
        self.planes_table.mark_square(first_head)
        for body_part in first_body:
            self.planes_table.mark_square(body_part)
        second_head = rnd.choice(self.planes_table.get_all_list())
        second_orientation = rnd.choice(self.planes_table[second_head])
        self._board.place_plane(second_head, second_orientation)

    def __getitem__(self, coords):
        return self._board[coords]

    def get_choice(self):
        if len(self._hits) == 0:
            for prob in range(4, 0, -1):
                prob_list = self._prob_reducer.get_prob_list(prob)
                if len(prob_list) > 0:
                    return rnd.choice(prob_list)
        else:
            try_list = []
            dir = [up(), down(), left(), right()]
            for hit in self._hits:
                for d in dir:
                    try:
                        new_sq = (hit[0] + d[0], hit[1] + d[1])
                        if new_sq not in self._hits and new_sq not in self._misses:
                            if len(self._prob_reducer[new_sq]) > 0:
                                try_list.append(new_sq)
                    except ValueError:
                        pass
            def by_prob(square):
                return len(self._prob_reducer[square])
            try_list = sorted(try_list, key = by_prob, reverse = True)
            if len(try_list) == 0:
                for prob in range(4, 0, -1):
                    prob_list = self._prob_reducer.get_prob_list(prob)
                    for hit in self._hits:
                        try:
                            prob_list.remove(hit)
                        except ValueError:
                            pass
                    if len(prob_list) > 0:
                        return rnd.choice(prob_list)
            else:
                return try_list[0]

    def was_miss(self, choice):
        self._prob_reducer.mark_square(choice)

    def was_hit(self, choice):
        self._hits.append(choice)

    def was_head(self, head, body):
        self._prob_reducer.mark_square(head)
        for part in body:
            self._prob_reducer.mark_square(part)
            try:
                self._hits.remove(part)
            except ValueError:
                pass
