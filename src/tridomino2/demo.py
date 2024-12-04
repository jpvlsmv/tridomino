from .work import GameBoard


def demo_rot():
    b = GameBoard(5,6)
    b.set(0,0,'%')
    b.set(0,5,'V')
    b.set(4,0,'>')

    print("\nOriginal board:")
    b.show()
    print("\nRotated 270")
    b.rotate270().show()

def demo_characterize():
    b = GameBoard(5,6)
    b.set(1,0,'>')
    b.set(1,1,'<')
    print("\nInitial Board:")
    b.show()
    print(f"characterized as {b.characterize()!r}")
    b2 = GameBoard(5,6)
    b2.set(3,4,'V')
    b2.set(4,4,'^')
    b2.set(3,3,'<')
    b2.set(3,2,'>')
    b2.show()
    print(f"characterized as {b2.characterize()!r}")
    reboard = GameBoard(0,0,stringrep=b2.characterize())
    reboard.show()

if __name__ == "__main__":
    #demo_rot()
    demo_characterize()
