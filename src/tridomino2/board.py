from __future__ import annotations

from dataclasses import dataclass
from itertools import chain, product
from typing import Generator, Optional

from parse import parse


class GameBoard:
    board: list[list[str]]
    gamerows: int
    gamecols: int
    empty: str

    def _north(self, r: int, c: int) -> tuple[int, int]:
        return r - 1, c

    def _south(self, r: int, c: int) -> tuple[int, int]:
        return r - 1, c

    def _east(self, r: int, c: int) -> tuple[int, int]:
        return r, c + 1

    def _west(self, r: int, c: int) -> tuple[int, int]:
        return r, c - 1

    def __init__(
        self,
        gamerows: int = 6,
        gamecols: int = 6,
        *,
        empty: str = " ",
        initial: Optional(str) = None,
        stringrep: Optional(str) = None,
    ):
        if stringrep is None:
            self.gamerows = gamerows
            self.gamecols = gamecols
            self.empty = empty
            if initial is None:
                self.board = [[empty for _ in range(gamecols)] for _ in range(gamerows)]
            else:
                self.board = [[initial[i][j] for j in range(gamecols)] for i in range(gamerows)]
        else:
            (r, c, bd) = parse("({:d}, {:d}, '{}')", stringrep)
            self.gamerows = r
            self.gamecols = c
            self.empty = empty
            self.board = [[bd[colidx + c * rowidx] for colidx in range(c)] for rowidx in range(r)]

    @dataclass
    class GamePos:
        row: int
        col: int

    def _available(self, p: GamePos) -> bool:
        """available positions are non-wall places that are empty"""
        return self.get(p.row, p.col) == self.empty

    def available(self, r: int, c: int) -> bool:
        """available cells are non-wall places that are empty"""
        return self._available(self.GamePos(r, c))

    def _occupied(self, p: GamePos) -> bool:
        return self.get(p.row, p.col) in ["v", "^", "<", ">"]

    def occupied(self, r: int, c: int) -> bool:
        """occupied cells have either a domino or partner, (not wall)"""
        return self._occupied(self.GamePos(r, c))

    def __str__(self) -> str:
        return "\n".join([(f'{"".join(r)}') for r in self.board])

    def __repr__(self) -> str:
        return str((self.gamerows, self.gamecols, "".join(chain(*self.board))))

    def show(self) -> None:
        res = "+" + "+".join(["-" for _ in range(self.gamecols)]) + "+\n"
        for r in self.board:
            res += "|" + " ".join(r) + "|\n"
        res += "+" + "+".join(["-" for _ in range(self.gamecols)]) + "+"
        return res

    def transpose(self):
        tb = GameBoard(self.gamecols, self.gamerows, empty=self.empty)
        for r, c in product(range(self.gamerows), range(self.gamecols)):
            p = self.get(r, c)
            pt = " "
            if p == ">":
                pt = "v"
            elif p == "<":
                pt = "^"
            elif p == "v":
                pt = ">"
            elif p == "^":
                pt = "<"
            else:
                pt = p
            tb.set(c, r, pt)
        return tb

    def rotate90(self):
        tb = GameBoard(self.gamecols, self.gamerows, empty=self.empty)
        for r, c in product(range(self.gamerows), range(self.gamecols)):
            p = self.get(r, c)
            pr = " "
            if p == ">":
                pr = "^"
            elif p == "<":
                pr = "v"
            elif p == "v":
                pr = ">"
            elif p == "^":
                pr = "<"
            else:
                pr = p
            tb.set(tb.gamerows - 1 - c, r, pr)
        return tb

    def rotate180(self):
        return self.rotate90().rotate90()

    def rotate270(self):
        return self.rotate90().rotate90().rotate90()

    def characterize(self) -> str:
        # Trim off all blank rows and columns
        b = GameBoard(self.gamerows, self.gamecols, initial=self.board)
        while all(b.available(0, c) for c in range(b.gamecols)):
            # Remove empty row from top of board
            b.board.pop(0)
            b.gamerows -= 1
        while all(b.available(b.gamerows - 1, c) for c in range(b.gamecols)):
            # Remove empty row from bottom of board
            b.board.pop()
            b.gamerows -= 1
        while all(b.available(r, 0) for r in range(b.gamerows)):
            # Remove empty column from left side
            for r in range(b.gamerows):
                b.board[r] = b.board[r][1:]
            b.gamecols -= 1
        while all(b.available(r, b.gamecols - 1) for r in range(b.gamerows)):
            # Remove empty column from right side
            for r in range(b.gamerows):
                b.board[r] = b.board[r][:-1]
            b.gamecols -= 1
        # Compare board to its symmetries, and return the lexicographically first
        # I, T, R90, R180, R270, TR90, TR180, TR270
        translate = b.transpose()
        i = repr(b)
        t = repr(translate)
        r90 = repr(b.rotate90())
        r180 = repr(b.rotate180())
        r270 = repr(b.rotate270())
        t90 = repr(translate.rotate90())
        t180 = repr(translate.rotate180())
        t270 = repr(translate.rotate270())
        #        for c in [i,t,r90,r180,r270,t90,t180,t270]:
        #            GameBoard(0,0,stringrep=c).show()
        return max([i, t, r90, r180, r270, t90, t180, t270])

    def set(self, rpos: int, cpos: int, value: str = "x") -> None:
        if not (0 <= rpos < self.gamerows) or not (0 <= cpos < self.gamecols):
            raise ValueError
        self.board[rpos][cpos] = value

    def _get(self, p: GamePos) -> str | None:
        if 0 <= p.row < self.gamerows and 0 <= p.col < self.gamecols:
            # Empty or occupied
            return self.board[p.row][p.col]
        # Out of bounds, return wall
        return "*"

    def get(self, r: int, c: int) -> str | None:
        return self._get(self.GamePos(r, c))

    def place(self, dom: Domino) -> GameBoard:
        nb = GameBoard(self.gamerows, self.gamecols, initial=self.board)
        if dom.orientation == "H":
            nb.set(dom.r, dom.c, ">")
            nb.set(dom.r, dom.c + 1, "<")
        else:  # if dom.orientation == "V":
            nb.set(dom.r, dom.c, "v")
            nb.set(dom.r + 1, dom.c, "^")
        return nb

    def places(self) -> Generator:
        blankboard = all(self.get(r, c) == self.empty for r, c in product(range(self.gamerows), range(self.gamecols)))
        for row, col, o in product(range(self.gamerows), range(self.gamecols), ["H", "V"]):
            d = Domino(row, col, o)
            pr, pc = d.partner()

            # Are the domino locations available?
            if not (self.available(d.r, d.c) and self.available(pr, pc)):
                continue

            if blankboard or self._connected(d):
                yield d

    def _connected(self, d: Domino) -> bool:
        "Returns True if domino d could be added to non-empty board b"
        pr, pc = d.partner()
        if not self.available(d.r, d.c) or not self.available(pr, pc):
            return False
        if (
            (self.occupied(*self._north(d.r, d.c)) or self.occupied(*self._north(pr, pc)))
            or (self.occupied(*self._south(d.r, d.c)) or self.occupied(*self._south(pr, pc)))
            or (self.occupied(*self._east(d.r, d.c)) or self.occupied(*self._east(pr, pc)))
            or (self.occupied(*self._west(d.r, d.c)) or self.occupied(*self._west(pr, pc)))
        ):
            return True
        return False

    def is_tridomino(self) -> bool:
        # Since I'm only creating connected positions, we assume validity
        return True


@dataclass
class Domino:
    r: int
    c: int
    orientation: str

    def partner(self) -> tuple[int, int]:
        if self.orientation == "H":
            return self.r, self.c + 1
        # else: # self.orientation == "V":
        return self.r + 1, self.c
