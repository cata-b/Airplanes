import unittest
from HistoryBoard import HistoryBoard

class Test_test_HistoryBoard(unittest.TestCase):
    def test___init__(self):
        hb = HistoryBoard()
        self.assertNotEqual(hb, None)

    def test___getitem__(self):
        hb = HistoryBoard()
        self.assertEqual(hb[1, 1], "")
        hb.mark_plane((1, 1))
        self.assertEqual(hb[1, 1], "P")
        hb.mark_hit((1, 1))
        self.assertEqual(hb[1, 1], "H")
        hb.mark_miss((1, 1))
        self.assertEqual(hb[1, 1], "M")
if __name__ == '__main__':
    unittest.main()
