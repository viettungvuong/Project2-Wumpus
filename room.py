from logic import Atomic, Or, And, Iff, Not, If


class Room:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n

        self.parent = None

        self.surrounding_rooms = []

        if x > 0:
            self.surrounding_rooms.append((x - 1, y))
        if x < n - 1:
            self.surrounding_rooms.append((x + 1, y))
        if y > 0:
            self.surrounding_rooms.append((x, y - 1))
        if y < n - 1:
            self.surrounding_rooms.append((x, y + 1))

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, __value) -> bool:
        if not isinstance(__value, Room):
            return False
        return self.x == __value.x and self.y == __value.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def relationship(self, kb):
        # relationship pit breeze
        left = Atomic(f"B{self.x},{self.y}")
        right = None
        for r in self.surrounding_rooms:
            if right is None:
                right = Atomic(f"P{r[0]},{r[1]}")
            else:
                right = Or(right, Atomic(f"P{r[0]},{r[1]}"))
        kb.add_sentence(Iff(left, right))

        left = Atomic(f"P{self.x},{self.y}")
        right = None
        for r in self.surrounding_rooms:
            if right is None:
                right = Atomic(f"B{r[0]},{r[1]}")
            else:
                right = And(right, Atomic(f"B{r[0]},{r[1]}"))
        kb.add_sentence(If(left, right))

        # relationship stench wumpus
        left = Atomic(f"S{self.x},{self.y}")
        right = None
        for r in self.surrounding_rooms:
            if right is None:
                right = Atomic(f"W{r[0]},{r[1]}")
            else:
                right = Or(right, Atomic(f"w{r[0]},{r[1]}"))
        kb.add_sentence(Iff(left, right))

        # if there is wumpus in a room, there is stench in surrounding rooms
        left = Atomic(f"W{self.x},{self.y}")
        right = None
        for r in self.surrounding_rooms:
            if right is None:
                right = Atomic(f"S{r[0]},{r[1]}")
            else:
                right = And(right, Atomic(f"S{r[0]},{r[1]}"))
        kb.add_sentence(If(left, right))
