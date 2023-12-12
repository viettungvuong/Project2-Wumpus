from sympy import symbols, Function, satisfiable
from sympy.logic.boolalg import And, Implies, Not, Or
import kb
from logic import modus_ponens

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

        self.agent = False

        self.visited = False

        self.surrounding_rooms = []

        if x > 0:
            self.surrounding_rooms.append((x - 1, y))
        if x < 9:
            self.surrounding_rooms.append((x + 1, y))
        if y > 0:
            self.surrounding_rooms.append((x, y - 1))
        if y < 9:
            self.surrounding_rooms.append((x, y + 1))

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
        self.wumpus = Not(self.wumpus)

    def check_pit(self):
        return {kb.pitF.subs({kb.x: self.x, kb.y: self.y}): self.pit}

    def check_wumpus(self):
        return {kb.wumpusF.subs({kb.x: self.x, kb.y: self.y}): self.wumpus}

    def check_stench(self):
        return {kb.stenchF.subs({kb.x: self.x, kb.y: self.y}): self.stench}

    def check_breeze(self):
        return {kb.breezeF.subs({kb.x: self.x, kb.y: self.y}): self.breeze}



room = Room(0, 0)
# room.set_room("W")
print(room.check_wumpus())

print(modus_ponens(Implies(kb.breezeF, kb.pitF), kb.breezeF))