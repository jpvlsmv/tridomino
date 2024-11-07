from dataclasses import dataclass
from itertools import chain, product 

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
            return r-1,c
    def _west(self, r: int,c: int) -> tuple[int, int]:
            return r-1,c

    def __init__(self, gamerows = 6, gamecols = 6, *, empty=" ", initial=None):
        self.gamerows = gamerows
        self.gamecols = gamecols
        self.empty = empty
        if initial is None:
            self.board = [
                [ '*' for _ in range(gamecols+2) ], # First row border
               * [ [ empty for _ in range(gamecols+2)] for _ in range(gamerows)],
                [ '*' for _ in range(gamecols+2) ] # Last row border
            ]
            for r in range(gamerows+2):
                self.board[r][0] = '*'
                self.board[r][gamecols+1] = '*'
        else:
            self.board = [ [ initial[i][j] for j in range(gamecols+2) ] for i in range(gamerows+2) ]

    @dataclass
    class gamepos:
        row: int
        col: int

    def _occupied(self, p: gamepos) -> bool|None:
        if self.board[p.row+1][p.col+1] == self.empty:
            return False
        if self.board[p.row+1][p.col+1] != '*':
            return True
    def occupied(self, r:int, c:int) -> bool|None:
        return self._occupied(self.gamepos(r,c))

    def __str__(self) -> str:
        return '\n'.join( [ (f'{"".join(r)}') for r in self.board])
    
    def __repr__(self) -> str:
        return str( (self.gamerows, self.gamecols, ''.join(chain(*self.board))) )

    def set(self, rpos:int, cpos:int, value:str ='x') -> None:
        assert(rpos < self.gamerows and cpos < self.gamecols)
        assert(self.occupied(rpos,cpos) == False)
        if rpos <= self.gamerows and cpos <= self.gamecols:
            self.board[rpos+1][cpos+1] = value

    def get(self, d: tuple[int,int]) -> str|None:
        assert(d[0] < self.gamerows+1 and d[1] < self.gamecols+1)
        if d[0] <= self.gamerows and d[1] <= self.gamecols:
            return self.board[d[0]+1][d[1]+1]
        return '*'

    def place(self, dom: "domino") -> "GameBoard":
        nb = GameBoard(self.gamerows, self.gamecols,initial=self.board)
        if dom.orientation == "H":
            nb.set(dom.r,dom.c,'>')
            nb.set(dom.r,dom.c+1,'<')
        if dom.orientation == "V":
            nb.set(dom.r,dom.c,'V')
            nb.set(dom.r+1,dom.c,'^')
        return nb

    def places(self) -> "domino":
        for row,col,o in product(range(self.gamerows),range(self.gamecols), ['H','V']):
            d = domino(row,col,o)
            pr, pc = d.partner()

            # Are the domino locations empty?
            if self.get((d.r, d.c)) != self.empty or self.get((pr, pc)) != self.empty:
                continue
            
            # a domino is connected if the (pre-)existing board has a domino to the north, south, west or east of either
            # its location, or the partner location
            if self.get(self._north(d.r, d.c)) != self.empty or self.get(self._north(pr, pc)) != self.empty:
                yield d
            elif self.get(self._south(d.r, d.c)) != self.empty or self.get(self._south(pr, pc)) != self.empty:
                yield d
            elif self.get(self._east(d.r, d.c)) != self.empty or self.get(self._east(pr, pc)) != self.empty:
                yield d
            elif self.get(self._west(d.r, d.c)) != self.empty or self.get(self._west(pr, pc)) != self.empty:
                yield d

            # Could have an empty board
            elif all([self.board[row][col] == self.empty for r,c in product(range(self.gamerows),range(self.gamecols))]):
                yield d


    def is_tridomino(self) -> bool:
        # A tridomino has exactly 3 dominos, and all cells are connected by edges
        cells = [ x for x in chain(*self.board) if x in ['V','>'] ]
        if len(cells) != 3:
            return False
        return True

@dataclass
class domino:
    r: int
    c: int
    orientation: str

    def partner(self) -> tuple[int, int]:
        if self.orientation == "H":
            return self.r, self.c+1
        if self.orientation == "V":
            return self.r+1, self.c
        return None

found = set()
nFound = 0

if __name__ == "__main__":
    b = GameBoard(2,4)
    for p1 in b.places():
        b1 = b.place(p1)
        for p2 in b1.places():
            b2 = b1.place(p2)
            for p3 in b2.places():
                b3 = b2.place(p3)
                if repr(b3) in found:
                    pass
                else:
                    click.echo(f'\nBoard {nFound}:\n{b3}')
                    found.add(repr(b3))
                    if b3.is_tridomino():
                        nFound += 1
                        click.echo('FOUND A 3-DOMINO CONFIG')
    click.echo(f'Considered a total of {len(found)} distinct boards, with {nFound} from tridominos')
