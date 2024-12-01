from .work import GameBoard

if __name__ == "__main__":
    b = GameBoard(5,6)
    b.set(0,0,'%')
    b.set(0,5,'V')
    b.set(4,0,'>')

    print("\nOriginal board:")
    b.show()
    print("\nRotated 270")
    b.R270().show()