import click
from tridomino2.board import GameBoard

def walk(b:GameBoard):
    p = list(b.places())
    if p is None:
        return None
    res = []
    for d in p:
        g = GameBoard(0,0,stringrep=repr(b))
        g.place(p)
        res.append(g)
    return res

def main() -> None:
    click.echo("Preparing to search")
    b = GameBoard(2,3)
    click.echo("\n".join(repr(_) for _ in walk(b)))

if __name__ == "__main__":
    main()