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

    def set_room(self, str):
        if str.__contains__("W"):
            self.wumpus = True
        if str.__contains__("G"):
            self.gold = True
        if str.__contains__("P"):
            self.pit = True
        if str.__contains__("B"):
            self.breeze = True
        if str.__contains__("S"):
            self.stench = True
        if str.__contains__("A"):
            self.agent = True

    def wumpus_hit(self):
        self.wumpus = False