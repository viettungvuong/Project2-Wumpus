rooms = set()

class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.wumpus = False
        self.gold = False
        self.pit = False
        self.breeze = False
        self.stench = False
        self.bat = False

        self.agent = False

        self.visited = False