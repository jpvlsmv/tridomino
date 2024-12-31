import click

from tridomino2.board import GameBoard

MARKERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def visit(b: GameBoard, depth: int = 0):
    potential_locations = list(b.places(marker=MARKERS[0:int(depth/2)]))
    print(f"{ "  " * depth}Visit to board {b=!r}, found {len(potential_locations)}")
    if len(potential_locations) == 0:
        if b.is_full():
            click.echo(f"{ "  " * depth}Found full board:\n{b.show()}")
            yield b
        else:
            click.echo(f"{ "  " * depth}Board not full\n{b.show()}")
            # discard b
    for d in potential_locations:
        g = b.place(d, value=MARKERS[int(depth / 2)])
        yield from visit(g, depth+1)


def main() -> None:
    click.echo("Preparing to search")
    b = GameBoard(2, 3)
    all_nodes = list(visit(b))
    click.echo("\n".join(repr(v) for v in all_nodes))


if __name__ == "__main__":
    main()
