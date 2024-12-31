import unittest

from tridomino2.board import GameBoard, Domino  # type: ignore


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.b = GameBoard(5, 6, initial="ABC><F" 
                                         "GHI  L"
                                         "MNOPQR"
                                         "STUvWX"
                                         "YZ0^23")

    def tearDown(self) -> None:
        del self.b
        return super().tearDown()

    def test_set_cell_value(self):
        self.b.set(2, 4, "A")
        assert self.b.occupied(2,4, by="A")
        self.b.set(2, 4, "Q")
        assert self.b.occupied(2,4, by="Q")

    def test_transpose(self):
        t = self.b.transpose()
        assert t.occupied(0,0, by=self.b.get(0,0))
        assert t.occupied(1,5, by=self.b.get(5,1))
        assert t.occupied(2,3, by=self.b.get(3,2))
        assert t.occupied(4,3, by=self.b.get(3,4))
        assert t.occupied(6,5, by=self.b.get(5,6))

    def test_rotate90(self):
        t = self.b.rotate90()
        assert t.occupied(1,2,by="Q")

    def test_rotate180(self):
        t = self.b.rotate180()
        assert t.occupied(1,2, by="^")

    def test_rotate270(self):
        t = self.b.rotate270()
        assert t.board[1][2] == "N"

    def test_available(self):
        assert self.b.available(1,3)
        assert self.b.available(1,4)

    def test_is_full(self):
        assert not self.b.is_full()
        f = self.b.place(Domino(1,3,"H"),"@" )
        assert f.is_full()

if __name__ == "__main__":
    unittest.main()
