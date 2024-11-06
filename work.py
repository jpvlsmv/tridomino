from dataclasses import dataclass
from pprint import pprint

class GameBoard:
    nRows: int
    nCols: int
    empty: str

    def __init__(self, nRows = 6, nCols = 6, *, empty=" ", initial=None):
        self.nRows = nRows
        self.nCols = nCols
        self.empty = empty
        if initial is None:
            self.board = [ [ empty for _ in range(nCols)] for _ in range(nRows)]
        else:
            self.board = [ [ initial[i][j] for j in range(nCols) ] for i in range(nRows) ]
            
    def __str__(self):
        return '\n'.join([
            f'+{"-+" * self.nCols}',
            * [ (f'|{"|".join(r)}|') for r in self.board],
            f'+{"-+" * self.nCols}'
        ])

    def set(self, rpos, cpos, value='x'):
        self.board[rpos][cpos] = value

    def place(self, dom: "domino"):
        nb = GameBoard(self.nRows, self.nCols,initial=self.board)
        if dom.orientation == "H":
            nb.set(dom.r,dom.c,'>')
            nb.set(dom.r,dom.c+1,'<')
        if dom.orientation == "V":
            nb.set(dom.r,dom.c,'V')
            nb.set(dom.r+1,dom.c,'^')
        return nb

    def places(self):
        for i in range(self.nRows):
            for j in range(self.nCols-1):
                if self.board[i][j] == self.empty and self.board[i][j+1] == self.empty:
                        yield domino(i,j,'H')
        for i in range(self.nRows-1):
            for j in range(self.nCols):
                if self.board[i][j] == self.empty and self.board[i+1][j] == self.empty:
                        yield domino(i,j,'V')

    def is_tridomino(self):
        return False

@dataclass
class domino:
    r: int
    c: int
    orientation: str

found = set()

if __name__ == "__main__":
    b = GameBoard(2,4)
    for p1 in b.places():
        b1 = b.place(p1)
        for p2 in b1.places():
            b2 = b1.place(p2)
            for p3 in b2.places():
                b3 = b2.place(p3)
                if repr(b3.board) in found:
                    pass
                else:
                    print(b3)
                    found.add(repr(b3.board))

                    if b3.is_tridomino():
                        print(f'FOUND A TRIDOMINO CONFIG')
    print(f'Found a total of {len(found)} distinct boards')