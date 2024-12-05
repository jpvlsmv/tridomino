import unittest

from tridomino2.work import GameBoard  # type: ignore


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.b = GameBoard(5, 6, initial=["ABC><F", "GHIJKL", "MNOPQR", "STUVWX", "YZ0^23"])

    def tearDown(self) -> None:
        del self.b
        return super().tearDown()

    def test_set_cell_value(self):
        self.b.set(2, 4, "A")
        assert self.b.board[2][4] == "A"
        self.b.set(2, 4, "Q")
        assert self.b.board[2][4] == "Q"

    def test_translate(self):
        t = self.b.transpose()
        assert t.board[2][3] == self.b.board[3][2]

    def test_rotate90(self):
        t = self.b.rotate90()
        assert t.board[1][2] == "Q"

    def test_rotate180(self):
        t = self.b.rotate180()
        assert t.board[1][2] == "V"

    def test_rotate270(self):
        t = self.b.rotate270()
        assert t.board[1][2] == "N"


if __name__ == "__main__":
    unittest.main()
