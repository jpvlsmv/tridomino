from __future__ import annotations

import click

from tridomino2.board import GameBoard

found = {}
nconsidered = 0

if __name__ == "__main__":
    b = GameBoard(6, 6)
    for dom1 in list(b.places()):
        boardwith1 = b.place(dom1)
        for dom2 in list(boardwith1.places()):
            boardwith2 = boardwith1.place(dom2)
            for dom3 in list(boardwith2.places()):
                boardwith3 = boardwith2.place(dom3)
                nconsidered += 1
                if boardwith3.characterize() in found:
                    found[(boardwith3.characterize())] += 1
                    # click.echo(f'{boardwith3!r} now seen {found[boardwith3.characterize()]} times')
                else:
                    found[(boardwith3.characterize())] = 1
    # click.echo(f'Found a total of {len(found)} distinct boards, after considering {nconsidered}')

    distinct = set()
    for k in found:
        b = GameBoard(0, 0, stringrep=k.translate(str.maketrans("v^><", "@@@@")))
        if b.characterize() not in distinct:
            distinct.add(b.characterize())

    click.echo("\n".join(sorted(distinct)))
    click.echo(f"A total of {len(distinct)} tridominos")
