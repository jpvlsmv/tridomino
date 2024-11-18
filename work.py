from __future__ import annotations

from dataclasses import dataclass
from itertools import chain, product
from typing import Generator

import click


class GameBoard:
    board: list[list[str]]
    gamerows: int
    gamecols: int
    empty: str

    def _north(self, r: int,c: int) -> tuple[int, int]:
            return r-1,c
    def _south(self, r: int,c: int) -> tuple[int, int]:
            return r-1,c
    def _east(self, r: int,c: int) -> tuple[int, int]:
            return r,c+1
    def _west(self, r: int,c: int) -> tuple[int, int]:
            return r,c-1

    def __init__(self, gamerows = 6, gamecols = 6, *, empty=" ", initial=None):
        self.gamerows = gamerows
        self.gamecols = gamecols
        self.empty = empty
        if initial is None:
            self.board = [ [ empty for _ in range(gamecols)] for _ in range(gamerows)]
        else:
            self.board = [ [ initial[i][j] for j in range(gamecols) ] for i in range(gamerows) ]

    @dataclass
    class GamePos:
        row: int
        col: int

    def _available(self, p: GamePos) -> bool:
        """ available positions are non-wall places that are empty"""
        return self.get(p.row,p.col) == self.empty

    def available(self, r:int, c:int) -> bool:
        """ available cells are non-wall places that are empty"""
        return self._available(self.GamePos(r,c))

    def _occupied(self, p:GamePos) -> bool:
        return self.get(p.row,p.col) in [ 'V', '^', '<', '>' ]
    def occupied(self, r:int, c:int) -> bool:
        """ occupied cells have either a domino or partner, (not wall) """
        return self._occupied(self.GamePos(r,c))

    def __str__(self) -> str:
        return '\n'.join( [ (f'{"".join(r)}') for r in self.board])

    def __repr__(self) -> str:
        return str( (self.gamerows, self.gamecols, ''.join(chain(*self.board))) )

    def T(self):
        tb = GameBoard(self.gamecols, self.gamerows, empty=self.empty)
        for r,c in product(range(self.gamerows), range(self.gamecols)):
            p = self.get(r,c)
            pT = ' '
            if p == '>': pT = 'V'
            elif p == '<': pT = '^'
            elif p == 'V': pT = '>'
            elif p == '^': pT = '<'
            tb.set(c,r, pT)
        return tb

    def characterize(self) -> str:
        # Trim off all blank rows and columns
        b = GameBoard(self.gamerows, self.gamecols, initial=self.board)
        click.echo(f'initial board is {repr(b)}')
        while all([b.available(0,c) for c in range(b.gamecols)]):
            # Remove empty row from top of board
            b.board.pop(0)
            b.gamerows -= 1
            click.echo(f'trimmed board is {repr(b)}')
        while all([b.available(b.gamerows-1,c) for c in range(b.gamecols)]):
            # Remove empty row from bottom of board
            b.board.pop()
            b.gamerows -= 1
            click.echo(f'trimmed board is {repr(b)}')
        while all([b.available(r,0) for r in range(b.gamerows)]):
            # Remove empty column from left side
            for r in range(b.gamerows):
                b.board[r] = b.board[r][1:]
            b.gamecols -= 1
            click.echo(f'trimmed board is {repr(b)}')
        while all([b.available(r,b.gamecols-1) for r in range(b.gamerows)]):
            # Remove empty column from right side
            for r in range(b.gamerows):
                b.board[r] = b.board[r][:-1]
            b.gamecols -= 1
            click.echo(f'trimmed board is {repr(b)}')
        # Compare board to its symmetries, and return the lexicographically first
        # I, T, R90, R180, R270, TR90, TR180, TR270
        identity = repr(b)
        translate = repr(b.T())
        click.echo(f'Translated board is {translate}')
        return min([identity,translate])

    def set(self, rpos:int, cpos:int, value:str ='x') -> None:
        assert (0 <= rpos < self.gamerows)
        assert (0 <= cpos < self.gamecols)
        if 0 <= rpos < self.gamerows and 0 <= cpos < self.gamecols:
            self.board[rpos][cpos] = value

    def _get(self, p: GamePos) -> str|None:
        if 0 <= p.row < self.gamerows and 0 <= p.col < self.gamecols:
            # Empty or occupied
            return self.board[p.row][p.col]
        # Out of bounds, return wall
        return '*'
    def get(self, r: int, c:int) -> str|None:
        return self._get(self.GamePos(r,c))

    def place(self, dom: Domino) -> GameBoard:
        nb = GameBoard(self.gamerows, self.gamecols,initial=self.board)
        if dom.orientation == "H":
            nb.set(dom.r,dom.c,'>')
            nb.set(dom.r,dom.c+1,'<')
        if dom.orientation == "V":
            nb.set(dom.r,dom.c,'V')
            nb.set(dom.r+1,dom.c,'^')
        return nb

    def places(self) -> Generator:
        blankboard = all([ self.get(r,c)==self.empty for r,c in product(range(self.gamerows),range(self.gamecols))])
        for row,col,o in product(range(self.gamerows),range(self.gamecols), ['H','V']):
            d = Domino(row,col,o)
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
        if  (self.occupied(*self._north(d.r, d.c)) or self.occupied(*self._north(pr, pc))) or \
            (self.occupied(*self._south(d.r, d.c)) or self.occupied(*self._south(pr, pc))) or \
            (self.occupied(*self._east (d.r, d.c)) or self.occupied(*self._east (pr, pc))) or \
            (self.occupied(*self._west (d.r, d.c)) or self.occupied(*self._west (pr, pc))):
                return True
        return False

    def is_tridomino(self) -> bool:
        # A tridomino has exactly 3 dominos, and all cells are connected by edges
        cells = [ x for x in chain(*self.board) if x in ['V','>'] ]
        if len(cells) != 3:
            return False
        return True

@dataclass
class Domino:
    r: int
    c: int
    orientation: str

    def partner(self) -> tuple[int, int]:
        if self.orientation == "H":
            return self.r, self.c+1
        else: # self.orientation == "V":
            return self.r+1, self.c

found = set()
nfound = 0

if __name__ == "__main__":
    b = GameBoard(2,4)
    for dom1 in list(b.places()):
        boardwith1 = b.place(dom1)
        for dom2 in list(boardwith1.places()):
            boardwith2 = boardwith1.place(dom2)
            for dom3 in list(boardwith2.places()):
                boardwith3 = boardwith2.place(dom3)
                click.echo(f'board {repr(boardwith3)} characterizes to {boardwith3.characterize()}')
                if boardwith3.characterize() in found:
                    click.echo(f'{repr(boardwith3)} already seen')
                else:
                    click.echo(f'\nBoard {nfound}:\n{boardwith3}')
                    found.add(boardwith3.characterize())
                    if boardwith3.is_tridomino():
                        nfound += 1
                        click.echo('FOUND A 3-DOMINO CONFIG')
    click.echo(f'Considered a total of {len(found)} distinct boards, with {nfound} from tridominos')
