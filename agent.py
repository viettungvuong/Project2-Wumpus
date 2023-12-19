from enum import Enum
from logic import Atomic, Not, Or
from room import Room
from kb import KB

import math
import copy
import random


class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4


class Map:
    def __init__(self):
        self.map = [[Room(i, j, 0) for j in range(10)] for i in range(10)]
        self.n = 0

    def get_room(self, x, y):
        return self.map[x][y]

    def heuristic(self, current_room, goal_room):
        return math.sqrt(
            (current_room.x - goal_room.x) ** 2 + (current_room.y - goal_room.y) ** 2
        )
        # euclidean distance

    def random_map(self):
        n = random.randint(3, 10)
        self.n = n
        self.map = [[Room(i, j, n) for j in range(n)] for i in range(n)]

        map_str = ["" for _ in range(n)]

        agent = None
        kb = KB()
        has_agent = False
        agent_pos = None

        for i in range(n):
            map_str[i] = ""
            for j in range(n):
                choice = random.randint(0, 15)
                if choice == 0:  # wumpus position
                    kb.add_sentence(Atomic(f"W{i},{j}"))
                    moves = self.map[i][j].surrounding_rooms
                    for move in moves:
                        kb.add_sentence(Atomic(f"S{move[0]},{move[1]}"))
                    map_str[i] += "W"
                elif choice == 1:
                    if i == 0 and j == 0:  # pit không thể ở chỗ ra khỏi cave
                        map_str[i] += "-"
                        if j < n - 1:
                            map_str[i] += "."
                        continue
                    kb.add_sentence(Atomic(f"P{i},{j}"))
                    moves = self.map[i][j].surrounding_rooms
                    for move in moves:
                        kb.add_sentence(Atomic(f"B{move[0]},{move[1]}"))
                    map_str[i] += "P"
                elif choice == 2:
                    kb.add_sentence(Atomic(f"G{i},{j}"))
                    map_str[i] += "G"
                elif choice == 3:
                    if has_agent == False:
                        agent_pos = (i, j)
                        has_agent = True
                        map_str[i] += "A"
                        kb.add_sentence(Not(Atomic(f"W{i},{j}")))
                        kb.add_sentence(Not(Atomic(f"P{i},{j}")))
                    else:
                        map_str[i] += "-"
                else:
                    map_str[i] += "-"

                if j < n - 1:
                    map_str[i] += "."

        for i in range(n):
            print(map_str[i])
        print("\n")

        agent = Agent(self.map[agent_pos[0]][agent_pos[1]], kb)
        agent.kb = kb
        return agent

    def read_map(self, file_name):
        try:
            with open(file_name, "r") as lines:
                n = int(lines.readline())
                self.n = n

                # 2d array representing the self.map
                self.map = [[Room(i, j, n) for j in range(n)] for i in range(n)]
                agent = None
                kb = KB()
                agent_pos = None

                for i in range(n):
                    line = lines.readline()
                    line_split = line.split(".")

                    for j in range(n):
                        if line_split[j].__contains__("A"):
                            kb.add_sentence(Not(Atomic(f"W{i},{j}")))
                            kb.add_sentence(Not(Atomic(f"P{i},{j}")))
                            agent_pos = (i, j)

                        elif line_split[j].__contains__("G"):
                            kb.add_sentence(Atomic(f"G{i},{j}"))

                        elif line_split[j].__contains__("W"):  # meet wumpus
                            kb.add_sentence(Atomic(f"W{i},{j}"))
                            moves = self.map[i][j].surrounding_rooms
                            for move in moves:
                                kb.add_sentence(Atomic(f"S{move[0]},{move[1]}"))

                        elif line_split[j].__contains__("P"):
                            kb.add_sentence(Atomic(f"P{i},{j}"))
                            moves = self.map[i][j].surrounding_rooms
                            for move in moves:
                                kb.add_sentence(Atomic(f"B{move[0]},{move[1]}"))

                agent = Agent(self.map[agent_pos[0]][agent_pos[1]], kb)
                agent.kb = kb
                return agent

        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
            return None


# below function return a room that is in the given direction from the current room
def room_direction(map, current_room, direction):
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
    def __init__(self, current_room, kb):
        self.current_room = None
        self.direction = Direction.RIGHT
        self.points = 0

        self.visited_rooms = []
        self.safe_rooms = []
        self.frontier = []

        self.alive = True

        self.achieved_golds = 0

        self.kb = kb

        self.move_to(current_room)

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
        self.expand_room(self.current_room)
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
        self.expand_room(next_room)
        self.visited_rooms.append(next_room)

    def shoot(self, next_room):
        # next_room = room_direction(self.current_room, self.direction)

        if next_room is not None:
            self.points -= 100
            x = next_room.x
            y = next_room.y
            if self.kb.check(Atomic(f"W{x},{y}")) == True:
                print("Wumpus screamed!")
                self.kb.remove(Atomic(f"W{x},{y}"))
                self.kb.remove(
                    Atomic(f"S{r[0]},{r[1]}")
                    for r in map.get_room(x, y).surrounding_rooms
                )

                self.kb.add_sentence(Not(Atomic(f"W{x},{y}")))
                self.kb.add_sentence(
                    Not(Atomic(f"S{r[0]},{r[1]}"))
                    for r in map.get_room(x, y).surrounding_rooms
                )
            else:
                print("You missed!")

    def percept(self):
        if self.kb.check(
            Atomic(f"W{self.current_room.x},{self.current_room.y}")
        ) or self.kb.check(Atomic(f"P{self.current_room.x},{self.current_room.y}")):
            self.points -= 10000
            self.alive = False
            print(f"You died at {self.current_room} - {self.current_room.parent}")
            return

        if self.kb.check(Atomic(f"G{self.current_room.x},{self.current_room.y}")):
            self.points += 10000
            self.achieved_golds += 1
            self.kb.remove(Atomic(f"G{self.current_room.x},{self.current_room.y}"))
            print(f"You collected gold at {self.current_room.x},{self.current_room.y}")

        if (
            self.kb.check(Atomic(f"B{self.current_room.x},{self.current_room.y}"))
            == False
        ):  # if not breeze then cannot be pit
            for r in self.current_room.surrounding_rooms:
                self.kb.add_sentence(Not(Atomic(f"P{r[0]},{r[1]}")))

        elif (
            self.kb.check(Atomic(f"B{self.current_room.x},{self.current_room.y}"))
            == True
        ):  # if not breeze then cannot be pit
            disjunction = None
            for r in self.current_room.surrounding_rooms:
                if disjunction is None:
                    disjunction = Atomic(f"P{r[0]},{r[1]}")
                else:
                    disjunction = Or(disjunction, Atomic(f"P{r[0]},{r[1]}"))

            self.kb.add_sentence(disjunction)

        if (
            self.kb.check(Atomic(f"S{self.current_room.x},{self.current_room.y}"))
            == False
        ):  # if not stench then cannmot be wumpus
            for r in self.current_room.surrounding_rooms:
                self.kb.add_sentence(Not(Atomic(f"W{r[0]},{r[1]}")))
        elif (
            self.kb.check(Atomic(f"S{self.current_room.x},{self.current_room.y}"))
            == True
        ):
            disjunction = None
            for r in self.current_room.surrounding_rooms:
                if disjunction is None:
                    disjunction = Atomic(f"W{r[0]},{r[1]}")
                else:
                    disjunction = Or(disjunction, Atomic(f"W{r[0]},{r[1]}"))

            self.kb.add_sentence(disjunction)

        map.get_room(self.current_room.x, self.current_room.y).relationship(self.kb)

    def expand_room(self, current_room):
        for r in current_room.surrounding_rooms:
            considering_room = copy.copy(
                map.get_room(r[0], r[1])
            )  # phải làm sao để mỗi thằng là một bản khác chứ không phải là reference tới thằng này
            if (
                considering_room not in self.visited_rooms
                and considering_room not in self.frontier
                and self.kb.backward_chaining(Atomic(f"P{r[0]},{r[1]}")) == False
            ):
                # thêm một cái giống node, lưu lại phòng trc của considering room (là room) để ta truy path
                if r[0] == 3 and r[1] == 4:
                    print(f"Considering room: {considering_room}")
                    print(self.kb.backward_chaining(Atomic(f"P{r[0]},{r[1]}")))
                considering_room.parent = current_room
                self.frontier.append(considering_room)

    def find_safe(self):
        for room in self.frontier:
            check_wumpus = Atomic(f"W{room.x},{room.y}")
            check_pit = Atomic(f"P{room.x},{room.y}")
            if (
                self.kb.check(Not(check_wumpus)) == True
                and self.kb.check(Not(check_pit)) == True
            ) or (
                self.kb.backward_chaining(check_wumpus) == False
                and self.kb.backward_chaining(check_pit) == False
            ):
                if room not in self.safe_rooms and room not in self.visited_rooms:
                    self.safe_rooms.append(room)

    def moves_trace(self, final_room):
        current = final_room
        path = []
        while current is not None:
            path.append(current)
            current = current.parent

        return path

    def solve(self):
        i = 0
        while self.alive:
            # nếu bị loop phòng (hai lần liên tiếp đều là 1 phòng) thì tìm đường ra cave
            print(
                f"Current room: {self.current_room} - Parent room: {self.current_room.parent is not None and self.current_room.parent}"
            )
            i += 1
            if self.alive == False:
                break

            self.find_safe()

            next_room = None

            if len(self.safe_rooms) > 0:
                next_room = self.safe_rooms.pop(0)

            else:
                # for r in self.current_room.surrounding_rooms:
                #     if (
                #         self.kb.check(Atomic(f"W{r[0]},{r[1]}"))
                #         or self.kb.backward_chaining(Atomic(f"W{r[0]},{r[1]}")) == True
                #     ):
                #         self.shoot(map.get_room(r[0], r[1]))  # shoot wumpus
                #         print(f"Shoot wumpus at ({r[0]}, {r[1]})")

                #     if (
                #         self.kb.check(Atomic(f"P{r[0]},{r[1]}")) == False
                #         and self.kb.backward_chaining(Atomic(f"P{r[0]},{r[1]}"))
                #         == False
                #     ):
                #         if map.get_room(r[0], r[1]) in self.visited_rooms:
                #             continue
                #         next_room = map.get_room(r[0], r[1])
                #         break
                for room in self.frontier:
                    r = (room.x, room.y)
                    if (
                        self.kb.check(Atomic(f"W{r[0]},{r[1]}"))
                        or self.kb.backward_chaining(Atomic(f"W{r[0]},{r[1]}")) == True
                    ):
                        if len(self.frontier) == 1:
                            self.shoot(map.get_room(r[0], r[1]))  # shoot wumpus
                            print(f"Shoot wumpus at ({r[0]}, {r[1]})")
                        else:
                            continue

                    if room in self.visited_rooms:
                        continue

                    next_room = room
                    break

            if next_room is None:  # xong hết rồi
                goal_room = self.exit_cave()
                # moves = self.moves_trace(goal_room)
                # while len(moves) > 0:
                #     move = moves.pop(-1)
                #     print(f"{move.x},{move.y}")
                break

            self.move_to(next_room)

        print(f"Final points: {self.points}")
        print(f"Total rooms visited: {i}")

    def exit_cave(self):
        # search from current room to the cave
        current_room = self.current_room

        self.visited_rooms.clear()
        self.frontier.clear()

        self.move_to(self.current_room)
        self.find_safe()

        print("Finding cave exit...")

        while current_room is None or not (current_room.x == 0 and current_room.y == 0):
            if current_room is not None:
                print(
                    f"Current room: {current_room} - Parent room: {current_room.parent is not None and current_room.parent}"
                )

            next_room = None

            if len(self.safe_rooms) > 0:
                self.safe_rooms = sorted(
                    self.safe_rooms,
                    key=lambda x: map.heuristic(
                        x, map.get_room(0, 0)
                    ),  # nhớ chỉnh index để 0, 0 thành 1, 1
                )

                next_room = self.safe_rooms.pop(0)

            else:
                self.frontier = sorted(
                    self.frontier,
                    key=lambda x: map.heuristic(
                        x, map.get_room(0, 0)
                    ),  # nhớ chỉnh index để 0, 0 thành 1, 1 theo đúng bài
                )

                # check wumpus pit
                index_pop = 0

                if len(self.frontier) == 0:
                    break

                room = self.frontier[index_pop]
                r = (room.x, room.y)

                if (
                    self.kb.check(Atomic(f"W{r[0]},{r[1]}"))
                    or self.kb.backward_chaining(Atomic(f"W{r[0]},{r[1]}")) == True
                ):  # chỉ nên shoot khi len = 1
                    self.shoot(self.frontier[index_pop])  # shoot wumpus
                    print(f"Shoot wumpus at ({r[0]}, {r[1]})")

                if next_room is None:
                    next_room = self.frontier.pop(index_pop)
                else:
                    if map.heuristic(
                        self.frontier[index_pop], map.get_room(0, 0)
                    ) < map.heuristic(next_room, map.get_room(0, 0)):
                        next_room = self.frontier.pop(index_pop)
                # print(f"Chosen room: {next_room}")
                # print(f"Visited: {next_room in self.visited_rooms}")

            current_room = copy.copy(next_room)
            self.move_to(current_room)

        self.points += 10
        print(f"Exit cave successfully")
        return current_room


map = Map()
agent = map.read_map("map2.txt")
if agent is not None:
    agent.solve()
