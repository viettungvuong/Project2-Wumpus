from enum import Enum

from logic import Atomic, Not
from main import map
from kb import KB


class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4


# below function return a room that is in the given direction from the current room
def room_direction(current_room, direction):
    if direction == Direction.FORWARD:
        if current_room.y >= 0:
            return map[current_room.x][current_room.y - 1]
        else:
            return None
    elif direction == Direction.BACKWARD:
        if current_room.y <= 9:
            return map[current_room.x][current_room.y + 1]
        else:
            return None
    elif direction == Direction.LEFT:
        if current_room.x >= 0:
            return map[current_room.x - 1][current_room.y]
        else:
            return None
    elif direction == Direction.RIGHT:
        if current_room.x <= 9:
            return map[current_room.x + 1][current_room.y + 1]
        else:
            return None


class Agent:
    def __init__(self, current_room):
        self.current_room = current_room
        self.direction = Direction.RIGHT
        self.points = 0

        self.kb = KB()
        # self.kb.add_sentence(Atomic(f"A{current_room.x},{current_room.y}"))
        self.kb.add_sentence(Not(Atomic(f"W{current_room.x},{current_room.y}")))
        self.kb.add_sentence(Not(Atomic(f"P{current_room.x},{current_room.y}")))

        self.percept()  # percept xung quanh

        self.visited_rooms = []
        self.safe_rooms = set()
        self.frontier = set()

        self.alive = True

        self.achieved_golds = 0

    def moves(self):
        return list(Direction)

    def move(self, direction):
        next_room = room_direction(self.current_room, direction)
        if next_room is not None:
            self.current_room = next_room
        else:
            return

        if self.kb.check(
            Atomic(f"W{self.current_room.x},{self.current_room.y}")
        ) or self.kb.check(Atomic(f"P{self.current_room.x},{self.current_room.y}")):
            print("You died!")
            return
        elif self.current_room.gold:
            print("You collected gold!")

        self.points -= 10
        self.percept()
        self.expand_room()
        self.visited_rooms.append(self.current_room)

    def move_to(self, next_room):
        if next_room in self.visited_rooms:
            return

        if next_room is not None:
            self.current_room = next_room
        else:
            return

        # self.points -= 10
        self.percept()
        self.expand_room()
        self.visited_rooms.append(self.current_room)

    def shoot(self):
        next_room = room_direction(self.current_room, self.direction)

        if next_room is not None:
            self.points -= 100
            x = next_room.x
            y = next_room.y
            if map[x][y].wumpus:
                print("Wumpus screamed!")
                map[x][y].wumpus = False
                self.kb.remove(Atomic(f"W{x},{y}"))
                self.kb.remove(
                    Atomic(f"S{r[0]},{r[1]}") for r in map[x][y].surrounding_rooms
                )

                self.kb.add_sentence(Not(Atomic(f"W{x},{y}")))
                self.kb.add_sentence(
                    Not(Atomic(f"S{r[0]},{r[1]}")) for r in map[x][y].surrounding_rooms
                )
            else:
                print("You missed!")

    def percept(self):
        if self.kb.check(
            Atomic(f"W{self.current_room.x},{self.current_room.y}")
        ) or self.kb.check(Atomic(f"P{self.current_room.x},{self.current_room.y}")):
            self.points -= 10000
            self.alive = False
            return

        if self.kb.check(Atomic(f"G{self.current_room.x},{self.current_room.y}")):
            self.points += 10000
            self.achieved_golds += 1

        if (
            self.kb.check(Not(Atomic(f"B{self.current_room.x},{self.current_room.y}")))
            and self.kb.backward_chaining(
                Not(Atomic(f"B{self.current_room.x},{self.current_room.y}"))
            )
            == False
        ):  # if not breeze
            for r in self.current_room.surrounding_rooms:
                self.kb.add_sentence(Not(Atomic(f"P{r[0]},{r[1]}")))

        if (
            self.kb.check(Not(Atomic(f"S{self.current_room.x},{self.current_room.y}")))
            and self.kb.backward_chaining(
                Not(Atomic(f"S{self.current_room.x},{self.current_room.y}"))
            )
            == False
        ):  # if not stench
            for r in self.current_room.surrounding_rooms:
                self.kb.add_sentence(Not(Atomic(f"W{r[0]},{r[1]}")))

    def find_safe(self):
        for room in self.frontier:
            check_wumpus = Not(Atomic(f"W{room.x},{room.y}"))
            check_pit = Not(Atomic(f"P{room.x},{room.y}"))
            if (
                self.kb.check(check_wumpus)
                and self.kb.check(check_pit)
                and self.kb.backward_chaining(check_wumpus) == False
                and self.kb.backward_chaining(check_pit) == False
            ):
                self.safe_rooms.add(room)

    def expand_room(self):
        for room in self.visited_rooms:
            for r in room.surrounding_rooms:
                considering_room = map[r[0]][r[1]]
                if (
                    considering_room not in self.visited_rooms
                    and considering_room not in self.frontier
                ):
                    # thêm một cái giống node, lưu lại phòng trc của considering room (là room) để ta truy path
                    self.frontier.add(considering_room)

    def moves_trace(self):
        return list(self.visited_rooms)

    def solve(self):
        while self.alive:
            self.percept()
            if self.alive == False:
                break

            self.find_safe()

            if len(self.safe_rooms) > 0:
                self.move_to(self.safe_rooms.pop(0))  # vao safe room

            else:
                # vao mot phong torng frontier
                # shoot wumpus
                for r in self.current_room.surrounding_rooms:
                    if (
                        self.kb.check(Atomic(f"W{r[0]},{r[1]}"))
                        or self.kb.backward_chaining(Atomic(f"W{r[0]},{r[1]}")) == True
                    ):
                        self.shoot()  # shoot wumpus
                        self.move_to(map[r[0]][r[1]])  # vao phong do
                        break
