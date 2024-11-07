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
    def _north(self, p: "gamepos") -> "gamepos":
            return gamepos(p.r-1,p.c)
    def _south(self, r: int,c: int) -> tuple[int, int]:
            return r+1,c
    def _south(self, p: "gamepos") -> "gamepos":
            return gamepos(p.r+1,p.c)
    def _east(self, r: int,c: int) -> tuple[int, int]:
            return r,c+1
    def _east(self, p: "gamepos") -> "gamepos":
            return gamepos(p.r,p.c+1)
    def _west(self, r: int,c: int) -> tuple[int, int]:
            return r,c-1
    def _west(self, p: "gamepos") -> "gamepos":
            return gamepos(p.r,p.c-1)

    def occupied_d(self, d: "domino") -> bool|None:
        if self.board[d.r+1][d.c+1][0] == '*':
            return None
        elif self.board[d.r+1][d.c+1][0] in 'Vv<>':
            return True
        pr, pc = d.partner()
        if self.board[pr+1][pc+1][0] == '*':
            return None
        elif self.board[pr+1][pc+1][0] in 'Vv<>':
            return True
        return False

    def occupied_sq(self, p: "gamepos") -> bool|None:
        if self.board[p.r+1][p.c+1][0] == '*':
            return None
        elif self.board[p.r+1][p.c+1][0] in 'Vv<>':
            return True
        return False

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

    def __str__(self) -> str:
        return '\n'.join( [ (f'{"".join(r)}') for r in self.board])
    
    def __repr__(self) -> str:
        return str( (self.gamerows, self.gamecols, ''.join(chain(*self.board))) )

    def set(self, rpos:int, cpos:int, value:str ='x') -> None:
        assert(not self.occupied_sq(gamepos(rpos,cpos)))
        if rpos <= self.gamerows and cpos <= self.gamecols:
            self.board[rpos+1][cpos+1] = value

    def get(self, d: tuple[int,int]) -> str|None:
        assert(d[0] < self.gamerows+1 and d[1] < self.gamecols+1)
        assert(self.occupied_sq(gamepos(d[0],d[1])))
        if d[0] <= self.gamerows and d[1] <= self.gamecols:
            return self.board[d[0]+1][d[1]+1]
        return '*'

    def place(self, dom: "domino") -> "GameBoard":
        assert(not self.occupied_sq(gamepos(dom.r,dom.c)))
        assert(not self.occupied_sq(gamepos(*dom.partner())))
        nb = GameBoard(self.gamerows, self.gamecols,initial=self.board)
        if dom.orientation == "H":
            nb.set(dom.r,dom.c,'>')
            nb.set(dom.r,dom.c+1,'<')
        if dom.orientation == "V":
            nb.set(dom.r,dom.c,'V')
            nb.set(dom.r+1,dom.c,'^')
        return nb

    def places(self):
        # Could have an empty board
        if all([not self.occupied_sq(gamepos(r,c)) for r,c, in product(range(self.gamerows),range(self.gamecols))]):
        #if all([self.get((r,c)) == self.empty for r,c in product(range(self.gamerows),range(self.gamecols))]):
            # yield all possible domino positions
            for drow,dcol,o in product(range(self.gamerows-1),range(self.gamecols), ['V']):  # Vertical in all but bottom row
                yield domino(drow,dcol,o)
            for drow,dcol,o in product(range(self.gamerows),range(self.gamecols-1), ['H']):  # Horizontal in all but right column
                yield domino(drow,dcol,o)
            return

        # Walk all row, col combinations and try each orientation
        for drow,dcol,o in product(range(self.gamerows),range(self.gamecols), ['H','V']):
            d = domino(drow,dcol,o)
            prow, pcol = d.partner()
            if prow >= self.gamerows or pcol >= self.gamecols:
                continue

            # Are the domino locations empty?
            if self.occupied_sq(gamepos(drow, dcol)) or self.occupied_sq(gamepos(prow, pcol)):
            #if self.get((row, col)) != self.empty or self.get((prow, pcol)) != self.empty:
                continue
            
            # a domino is connected if the (pre-)existing board has a domino to the north, south, west or east of either
            # its location, or the partner location
            if self.occupied_sq(self._north(gamepos(drow, dcol))) or self.occupied_sq(self._north(gamepos(prow, pcol))):
                yield d
            elif self.occupied_sq(self._south(gamepos(drow, dcol))) or self.occupied_sq(self._south(gamepos(prow, pcol))):
                yield d
            elif self.occupied_sq(self._east(gamepos(drow, dcol))) or self.occupied_sq(self._east(gamepos(prow, pcol))):
                yield d
            elif self.occupied_sq(self._west(gamepos(drow, dcol))) or self.occupied_sq(self._west(gamepos(prow, pcol))):
                yield d

@dataclass
class gamepos:
    r: int
    c: int

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


def tridomino_places(board: GameBoard):
    tridoms = dict()
    found = set()
    nFound = 0
    for p1 in b.places():
        b1 = b.place(p1)
        for p2 in b1.places():
            b2 = b1.place(p2)
            for p3 in b2.places():
                b3 = b2.place(p3)
                if repr(b3) in found:
                    pass
                else:
                    nFound += 1
                    click.echo(f'\nBoard {nFound}:\n{b3}')
                    shadow = repr(b3).translate(str.maketrans('><^V','XXXX'))
                    if shadow in tridoms:
                        click.echo(f'It is a duplicate of board {tridoms[shadow]}')
                    else:
                        tridoms[shadow] = nFound
                found.add(repr(b3))
    click.echo(f'Considered a total of {len(found)} distinct boards, with {len(tridoms)} tridominoes')
#    click.echo(f'Tridom boards: {tridoms=}')

if __name__ == "__main__":
    b = GameBoard(2,3)
    tridomino_places(b)