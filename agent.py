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
        # manhattan distance
        return abs(current_room.x - goal_room.x) + abs(current_room.y - goal_room.y)

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
                    # kb.add_sentence(Atomic(f"W{i},{j}"))
                    self.map[i][j].wumpus = True
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
                    # kb.add_sentence(Atomic(f"P{i},{j}"))
                    self.map[i][j].pit = True
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

                        if line_split[j].__contains__("G"):
                            kb.add_sentence(Atomic(f"G{i},{j}"))

                        if line_split[j].__contains__("W"):  # meet wumpus
                            # kb.add_sentence(Atomic(f"W{i},{j}"))
                            self.map[i][j].wumpus = True
                            moves = self.map[i][j].surrounding_rooms
                            for move in moves:
                                kb.add_sentence(Atomic(f"S{move[0]},{move[1]}"))
                        # else:
                        #     kb.add_sentence(Not(Atomic(f"W{i},{j}")))

                        if line_split[j].__contains__("P"):
                            # kb.add_sentence(Atomic(f"P{i},{j}"))
                            self.map[i][j].pit = True
                            moves = self.map[i][j].surrounding_rooms
                            for move in moves:
                                kb.add_sentence(Atomic(f"B{move[0]},{move[1]}"))
                        # else:
                        #     kb.add_sentence(Not(Atomic(f"P{i},{j}")))

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

    # def move(self, direction):
    #     next_room = room_direction(self.current_room, direction)
    #     if next_room is not None:
    #         self.current_room = next_room
    #     else:
    #         return

    #     if self.kb.check(
    #         Atomic(f"W{self.current_room.x},{self.current_room.y}")
    #     ) or self.kb.check(Atomic(f"P{self.current_room.x},{self.current_room.y}")):
    #         print("You died!")
    #         return
    #     elif self.current_room.gold:
    #         print("You collected gold!")

    #     self.points -= 10

    #     self.percept()
    #     self.expand_room(self.current_room)
    #     self.visited_rooms.append(self.current_room)

    def move_to(self, next_room):
        if next_room in self.visited_rooms:
            return

        if next_room is not None:
            self.current_room = next_room
        else:
            return

        # self.points -= 10
        percept = self.percept()
        self.expand_room(next_room)
        self.visited_rooms.append(next_room)
        return percept

    def shoot(self, next_room):
        # next_room = room_direction(self.current_room, self.direction)

        if next_room is not None:
            self.points -= 100
            x = next_room.x
            y = next_room.y
            if next_room.wumpus == True:
                print(f"Wumpus screamed at ({x}, {y})")
                self.kb.remove(Atomic(f"W{x},{y}"))
                next_room.wumpus = False
                self.kb.remove(
                    Atomic(f"S{r[0]},{r[1]}")
                    for r in map.get_room(x, y).surrounding_rooms
                )

                self.kb.add_sentence(Not(Atomic(f"W{x},{y}")))
                self.kb.add_sentence(
                    Not(Atomic(f"S{r[0]},{r[1]}"))
                    for r in map.get_room(x, y).surrounding_rooms
                )

    def percept(self):
        special = None

        if self.current_room.wumpus or self.current_room.pit:
            self.points -= 10000
            self.alive = False
            print(f"You died at {self.current_room} - {self.current_room.parent}")
            return (
                "W"
                if self.kb.check(
                    Atomic(f"W{self.current_room.x},{self.current_room.y}")
                )
                else "P"
            )

        if self.kb.check(Atomic(f"G{self.current_room.x},{self.current_room.y}")):
            self.points += 1000
            self.achieved_golds += 1
            self.kb.remove(Atomic(f"G{self.current_room.x},{self.current_room.y}"))
            special = "G"

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

        # map.get_room(self.current_room.x, self.current_room.y).relationship(self.kb)

        return special

    def expand_room(self, current_room):
        for r in current_room.surrounding_rooms:
            considering_room = copy.copy(
                map.get_room(r[0], r[1])
            )  # phải làm sao để mỗi thằng là một bản khác chứ không phải là reference tới thằng này
            if (
                considering_room not in self.visited_rooms
                and considering_room not in self.frontier
            ):
                considering_room.parent = current_room
                self.frontier.append(considering_room)

    def find_safe(self):
        for room in self.frontier:
            check_wumpus = Atomic(f"W{room.x},{room.y}")
            check_pit = Atomic(f"P{room.x},{room.y}")

            if self.kb.check(Not(check_wumpus)) and self.kb.check(Not(check_pit)):
                if room not in self.safe_rooms and room not in self.visited_rooms:
                    self.safe_rooms.append(room)
                    continue

            if self.check_safe(room) == True:
                if room not in self.safe_rooms and room not in self.visited_rooms:
                    self.safe_rooms.append(room)
                    continue

    # def moves_trace(self, moves):
    #     moves_copy = []
    #     moves_copy.extend(moves)

    #     moves_len = len(moves)

    #     for i in range(1, moves_len):
    #         room = moves[i][0]  # current room
    #         if i < moves_len - 1:
    #             next_room = moves[i + 1][0]
    #         if room.parent == next_room.parent:
    #             parent = copy.copy(room.parent)
    #             parent.parent = room
    #             moves_copy.insert(i + 1, (parent, None))
    #         else:
    #             # find parent of room
    #             common_parent = None

    #             current = copy.copy(room)
    #             current_next = copy.copy(next_room)
    #             current_list = [current]
    #             next_list = [current_next]
    #             while current.parent is not None and current_next.parent is not None:
    #                 current = current.parent
    #                 current_next = current_next.parent
    #                 current_list.append(current)
    #                 next_list.append(current_next)
    #                 if current in next_list:
    #                     common_parent = current
    #                     break
    #                 if current_next in current_list:
    #                     common_parent = current_next
    #                     break

    #             if common_parent is not None:
    #                 # traverse back from current to the common parent
    #                 current_index = i + 1

    #                 for current_trav in current_list:
    #                     if current_trav == room:  # current room
    #                         continue
    #                     moves_copy.insert(current_index, (current_trav, None))
    #                     current_index += 1

    #                 current_index = i + 1
    #                 next_list.reverse()  # traverse from the common parent to the next room

    #                 for current_trav in next_list:
    #                     if current_trav == common_parent:  # current room
    #                         continue
    #                     moves_copy.insert(current_index, (current_trav, None))
    #                     current_index = i + 1

    #     return moves_copy

    def check_safe(self, room):
        check_wumpus = Atomic(f"W{room.x},{room.y}")
        check_pit = Atomic(f"P{room.x},{room.y}")

        # if self.kb.resolution(check_wumpus) or self.kb.resolution(check_pit):
        #     # print(f"Found wumpus or pit at {room} - {room.parent}")
        #     return False

        if self.kb.resolution(Not(check_wumpus)) and self.kb.resolution(Not(check_pit)):
            # print(f"Not found wumpus or pit at {room} - {room.parent}")
            return True

        return False

    def solve(self):
        i = 0
        moves = [(self.current_room, "Start")]
        while self.alive:
            print(f"Current room: {self.current_room} - {self.current_room.parent}")
            i += 1
            if self.alive == False:
                break

            self.find_safe()

            next_room = None

            if len(self.safe_rooms) > 0:
                next_room = self.safe_rooms.pop(0)

            # else:
            # for r in self.current_room.surrounding_rooms:
            #     if (
            #         self.kb.check(Atomic(f"W{r[0]},{r[1]}"))
            #         or self.kb.forward_chaining(Atomic(f"W{r[0]},{r[1]}")) == True
            #     ):
            #         self.shoot(map.get_room(r[0], r[1]))  # shoot wumpus
            #         print(f"Shoot wumpus at ({r[0]}, {r[1]})")

            #     if (
            #         self.kb.check(Atomic(f"P{r[0]},{r[1]}")) == False
            #         and self.kb.forward_chaining(Atomic(f"P{r[0]},{r[1]}"))
            #         == False
            #     ):
            #         if map.get_room(r[0], r[1]) in self.visited_rooms:
            #             continue
            #         next_room = map.get_room(r[0], r[1])
            #         break
            else:
                for i in range(len(self.frontier)):
                    room = self.frontier[i]
                    r = (room.x, room.y)
                    # if room.wumpus == True:
                    #     # golds = self.locate_gold(room)  # tìm các gold

                    #     # # nếu có gold
                    #     # if len(golds) > 0:
                    #     #     if (
                    #     #         golds * 1000 > 100
                    #     #     ):  # nếu có nhiều gold và đủ đề bù phần bị mất do shoot arrow
                    #     #         # chi phí đi lại có đủ bù phần bị mất do shoot arrow
                    #     #         current = copy.copy(room)

                    #     #         cost = 0

                    #     #         for i in range(len(golds)):
                    #     #             golds = sorted(
                    #     #                 golds,
                    #     #                 key=lambda x: map.heuristic(current, x),
                    #     #             )
                    #     #             cost += map.heuristic(current, golds[0])
                    #     #             current = golds.pop(0)

                    #     #         cost += map.heuristic(
                    #     #             current, room
                    #     #         )  # chi phí đi lại từ gold cuối cùng về room

                    #     #         if cost < 100:
                    #     #             self.shoot(room)
                    #     #             print(f"Shoot wumpus at ({r[0]}, {r[1]})")

                    #     #     else:
                    #     #         continue

                    #     continue

                    if room in self.visited_rooms:
                        continue

                    if room.pit == True:
                        continue

                    if room.wumpus == True:
                        if len(self.frontier) == 1:
                            self.shoot(room)
                            print(f"Shoot wumpus at ({r[0]}, {r[1]})")
                        else:
                            continue

                    next_room = room
                    self.frontier.pop(i)
                    self.kb.add_sentence(Not(Atomic(f"W{r[0]},{r[1]}")))
                    self.kb.add_sentence(Not(Atomic(f"P{r[0]},{r[1]}")))
                    break

            if next_room is None:  # xong hết rồi
                self.exit_cave(moves)
                # moves = self.moves_trace(moves)
                # for room in moves:
                #     print(
                #         f"Move to {room[0]} (Parent: {room[0].parent}) {room[1] if room[1] is not None else ''}"
                #     )
                break

            move_to = self.move_to(next_room)
            moves.append((next_room, move_to))

        print(f"Final points: {self.points}")

    def exit_cave(self, moves):
        # search from current room to the cave
        current_room = self.current_room

        self.visited_rooms.clear()
        self.frontier.clear()

        self.move_to(self.current_room)
        self.find_safe()

        print("Finding cave exit...")

        while current_room is None or not (current_room.x == 0 and current_room.y == 0):
            print(f"Current room: {self.current_room} - {self.current_room.parent}")
            next_room = None
            shot_wumpus = False

            if len(self.safe_rooms) > 0:
                self.safe_rooms = sorted(
                    self.safe_rooms,
                    key=lambda x: map.heuristic(
                        x, map.get_room(0, 0)
                    ),  # nhớ chỉnh index để 0, 0 thành 1, 1
                )

                next_room = self.safe_rooms.pop(0)

            # else:
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

            if room.wumpus == True:  # chỉ nên shoot khi len = 1
                if len(self.frontier) == 1:
                    self.shoot(self.frontier[index_pop])  # shoot wumpus
                    shot_wumpus = True
                else:
                    index_pop += 1
                    continue

            if self.check_safe(room) == False or room in self.visited_rooms:
                index_pop += 1
                continue

            get_room = self.frontier[index_pop]

            if next_room is not None:
                if map.heuristic(get_room, map.get_room(0, 0)) > map.heuristic(
                    next_room, map.get_room(0, 0)
                ):
                    next_room = get_room
                    self.frontier.pop(index_pop)
            # print(f"Chosen room: {next_room}")
            # print(f"Visited: {next_room in self.visited_rooms}")

            current_room = copy.copy(next_room)
            self.kb.add_sentence(Not(Atomic(f"W{current_room.x},{current_room.y}")))
            self.kb.add_sentence(Not(Atomic(f"P{current_room.x},{current_room.y}")))
            move_to = self.move_to(current_room)

            if current_room.x == 0 and current_room.y == 0:
                move_to = "Exit"
            if shot_wumpus == True:
                if move_to is None:
                    move_to = "Shot Wumpus"
                else:
                    move_to += "Shot Wumpus"
            moves.append((current_room, move_to))

        self.points += 10
        print(f"Exit cave successfully")
        return current_room

    def locate_gold(self, starting_room):
        frontier = []
        visited_rooms = []
        visited_rooms.extend(self.visited_rooms)
        frontier.append(starting_room)

        gold = []

        while len(frontier) > 0:
            current_room = frontier.pop(-1)
            visited_rooms.append(current_room)

            if self.kb.check(Atomic(f"G{current_room.x},{current_room.y}")) == True:
                gold.append(current_room)

            for r in current_room.surrounding_rooms:
                if r not in visited_rooms:
                    frontier.append(map.get_room(r[0], r[1]))

        return gold


map = Map()
agent = map.random_map()
# agent = map.read_map("map3.txt")
if agent is not None:
    agent.solve()
