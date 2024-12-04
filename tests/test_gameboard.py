import unittest

from tridomino2.work import GameBoard


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.b = GameBoard(5,6, initial = [ "ABC><F", "GHIJKL", "MNOPQR", "STUVWX", "YZ0^23"])
    def tearDown(self) -> None:
        del self.b
        return super().tearDown()

    def test_set_cell_value(self):
        self.b.set(2,4,'A')
        assert(self.b.board[2][4] == 'A')
        print(f"\n{self.b}\n")
        self.b.set(2,4,'Q')

    def test_translate(self):
        t = self.b.transpose()
        print(f"\n{t}\n")

    def test_rotate90(self):
        t = self.b.rotate90()
        print(f"\n{t}\n")

    def test_rotate180(self):
        t = self.b.rotate180()
        print(f"\n{t}\n")

if __name__ == "__main__":
   unittest.main()
