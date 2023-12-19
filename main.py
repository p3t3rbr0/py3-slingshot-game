import os
import sys

from src.game import Game

if __name__ == "__main__":
    path = os.path.expanduser("~") + "/.slingshot"
    if not os.path.exists(path):
        os.mkdir(path)
    path += "/logfile.txt"
    sys.stderr = open(path, "w")
    sys.stdout = sys.stderr
    game = Game()
    game.run()
