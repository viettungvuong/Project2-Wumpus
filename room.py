from logic import Atomic, OR, IFF


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

    def __eq__(self, __value: object) -> bool:
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
                right = OR(right, Atomic(f"P{r[0]},{r[1]}"))
            kb.add_sentence(IFF(left, right))

        # relationship stench wumpus
        left = Atomic(f"S{self.x},{self.y}")

        right = None

        for r in self.surrounding_rooms:
            if right is None:
                right = Atomic(f"W{r[0]},{r[1]}")
            else:
                right = OR(right, Atomic(f"w{r[0]},{r[1]}"))
            kb.add_sentence(IFF(left, right))
