from sympy import symbols, Function, satisfiable
from sympy.logic.boolalg import And, Implies, Not, Or

rooms = set()

class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.wumpus = None
        self.gold = None
        self.pit = None
        self.breeze = None
        self.stench = None

        self.agent = None # agent currently here

        self.visited = False

        self.surrounding_rooms = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def set_room(self, str):
        if str.__contains__("W"):
            self.wumpus = symbols(f"Wumpus({self.x}, {self.y})")
        if str.__contains__("G"):
            self.gold = symbols(f"Gold({self.x}, {self.y})")
        if str.__contains__("P"):
            self.pit = symbols(f"Pit({self.x}, {self.y})")
        if str.__contains__("B"):
            self.breeze = symbols(f"Breeze({self.x}, {self.y})")
        if str.__contains__("S"):
            self.stench = symbols(f"Stench({self.x}, {self.y})")
        if str.__contains__("A"):
            self.agent = symbols(f"Agent({self.x}, {self.y})")

    def wumpus_hit(self):
        self.wumpus = Not(self.wumpus)

    def possible_wumpus(self):
        surrounding_wumpus = [symbols(f"Wumpus({r[0]}, {r[1]})") for r in self.surrounding_rooms]
        return Implies(self.stench, Or(*surrounding_wumpus))

    def possible_pit(self):
        surrounding_pit = [symbols(f"Pit({r[0]}, {r[1]})") for r in self.surrounding_rooms]
        return Implies(self.breeze, Or(*surrounding_pit))

    def has_wumpus(self):
        surrounding_stench = [symbols(f"Stench({r[0]}, {r[1]})") for r in self.surrounding_rooms]
        return Implies(self.wumpus, And(*surrounding_stench))

    def has_pit(self):
        surrounding_breeze = [symbols(f"Breeze({r[0]}, {r[1]})") for r in self.surrounding_rooms]
        return Implies(self.wumpus, And(*surrounding_breeze))