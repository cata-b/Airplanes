import unittest
from AirplaneBoard import AirplaneBoard
from DirectionsHelper import *
class Test_test_AirplaneBoard(unittest.TestCase):
    def test___init__(self):
        self.assertNotEqual(AirplaneBoard(), None)

    def test___getitem__(self):
        ab = AirplaneBoard()
        self.assertEqual(ab[1, 1], 0)
        ab.place_plane((1, 3), (-1, 0))
        self.assertEqual(ab[1, 3], 2)
        self.assertEqual(ab[2, 3], 1)

    def test_get_plane(self):
        ab = AirplaneBoard()
        with self.assertRaises(ValueError):
            ab.get_plane((1, 1))
        ab.place_plane((1, 3), (-1, 0))
        self.assertEqual(len(ab.get_plane((1, 3))), 9)

    def test_place_plane(self):
        ab = AirplaneBoard()
        ab.place_plane((1, 3), (-1, 0))
        with self.assertRaises(PermissionError):
            ab.place_plane((3, 4), right())


if __name__ == '__main__':
    unittest.main()
