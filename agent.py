from enum import Enum
from logic import Atomic, Not, Or
from room import Room
from kb import KB
import turtle

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
        self.golds = 0

    def get_room(self, x, y):
        return self.map[x][y]

    def heuristic(self, current_room, goal_room):
        # manhattan distance
        return abs(current_room.x - goal_room.x) + abs(current_room.y - goal_room.y)

    def random_map(self):
        n = random.randint(3, 7)
        self.n = n
        self.map = [[Room(i, j, n) for j in range(n)] for i in range(n)]

        map_str = ["" for _ in range(n)]

        agent = None
        kb = KB()

        has_agent = False
        agent_pos = None

        count_wumpus = 0
        count_pit = 0

        for i in range(n):
            map_str[i] = ""
            for j in range(n):
                # nếu chưa có agent, wumpus, pit, gold thì ưu tiên
                choice = random.randint(0, 15)
                if choice == 0:  # wumpus position
                    # kb.add_sentence(Atomic(f"W{i},{j}"))
                    self.map[i][j].wumpus = True
                    moves = self.map[i][j].surrounding_rooms
                    for move in moves:
                        kb.add_sentence(Atomic(f"S{move[0]},{move[1]}"))
                    map_str[i] += "W"
                    count_wumpus += 1
                elif choice == 1:  # pit position
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
                    count_pit += 1
                elif choice == 2:  # gold position
                    self.map[i][j].gold = True
                    kb.add_sentence(Not(Atomic(f"W{i},{j}")))
                    kb.add_sentence(Not(Atomic(f"P{i},{j}")))
                    kb.add_sentence(Atomic(f"G{i},{j}"))
                    map_str[i] += "G"
                    self.golds += 1
                elif choice == 3:  # agent position
                    if has_agent == False:
                        self.map[i][j].agent=True
                        has_agent = True
                        map_str[i] += "A"
                        kb.add_sentence(Not(Atomic(f"W{i},{j}")))
                        kb.add_sentence(Not(Atomic(f"P{i},{j}")))
                        agent_pos = (i, j)
                    else:
                        map_str[i] += "-"
                else:
                    map_str[i] += "-"

                if j < n - 1:
                    map_str[i] += "."

        if has_agent == False:  # nếu không có agent thì random
            while True:
                (i, j) = (random.randint(0, n - 1), random.randint(0, n - 1))
                if map_str[i][j * 2] == "-":
                    if kb.check(Atomic(f"G{i},{j}")) == False:
                        self.map[i][j].agent=True
                        map_str[i] = map_str[i][: j * 2] + "A" + map_str[i][j * 2 + 1 :]
                        kb.add_sentence(Not(Atomic(f"W{i},{j}")))
                        kb.add_sentence(Not(Atomic(f"P{i},{j}")))
                        has_agent = True
                        agent_pos = (i, j)
                        break

        if count_wumpus == 0:
            while True:
                (i, j) = (random.randint(0, n - 1), random.randint(0, n - 1))
                if map_str[i][j * 2] == "-":
                    map_str[i] = map_str[i][: j * 2] + "W" + map_str[i][j * 2 + 1 :]
                    for move in self.map[i][j].surrounding_rooms:
                        kb.add_sentence(Atomic(f"S{move[0]},{move[1]}"))
                    count_wumpus += 1
                    self.map[i][j].wumpus = True
                    break

        if count_pit == 0:
            while True:
                (i, j) = (random.randint(1, n - 1), random.randint(1, n - 1))
                if map_str[i][j * 2] == "-":
                    self.map[i][j].agent = True
                    map_str[i] = map_str[i][: j * 2] + "P" + map_str[i][j * 2 + 1 :]
                    for move in self.map[i][j].surrounding_rooms:
                        kb.add_sentence(Atomic(f"B{move[0]},{move[1]}"))
                    count_pit += 1
                    self.map[i][j].pit = True
                    break

        if self.golds == 0:
            while True:
                (i, j) = (random.randint(0, n - 1), random.randint(0, n - 1))
                if map_str[i][j * 2] == "-":
                    self.map[i][j].gold = True
                    map_str[i] = map_str[i][: j * 2] + "G" + map_str[i][j * 2 + 1 :]
                    kb.add_sentence(Not(Atomic(f"W{i},{j}")))
                    kb.add_sentence(Not(Atomic(f"P{i},{j}")))
                    kb.add_sentence(Atomic(f"G{i},{j}"))
                    self.golds += 1
                    break

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
                            self.map[i][j].agent= True
                            kb.add_sentence(Not(Atomic(f"W{i},{j}")))
                            kb.add_sentence(Not(Atomic(f"P{i},{j}")))
                            agent_pos = (i, j)

                        if line_split[j].__contains__("G"):
                            self.map[i][j].gold = True
                            self.golds += 1
                            kb.add_sentence(Atomic(f"G{i},{j}"))
                            kb.add_sentence(Not(Atomic(f"W{i},{j}")))
                            kb.add_sentence(Not(Atomic(f"P{i},{j}")))

                        if line_split[j].__contains__("W"):  # meet wumpus
                            # kb.add_sentence(Atomic(f"W{i},{j}"))
                            self.map[i][j].wumpus = True
                            moves = self.map[i][j].surrounding_rooms
                            for move in moves:
                                kb.add_sentence(Atomic(f"S{move[0]},{move[1]}"))

                        if line_split[j].__contains__("P"):
                            # kb.add_sentence(Atomic(f"P{i},{j}"))
                            self.map[i][j].pit = True
                            moves = self.map[i][j].surrounding_rooms
                            for move in moves:
                                kb.add_sentence(Atomic(f"B{move[0]},{move[1]}"))

                        # self.map[i][j].relationship(
                        #     kb
                        # )  # add relationship between rooms

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

        if current_room.wumpus:
            self.shoot(current_room)

        self.move_to(current_room)

    def moves(self):
        return list(Direction)

    def move_to(self, next_room):
        if next_room in self.visited_rooms:
            return

        if next_room is not None:
            self.current_room = next_room
        else:
            return

        self.points -= 10
        percept = self.percept()
        self.expand_room(next_room)
        self.visited_rooms.append(next_room)
        return percept

    def shoot(self, next_room):
        if next_room is not None:
            self.points -= 100
            x = next_room.x
            y = next_room.y
            if next_room.wumpus == True:
                print(f"Wumpus screamed at {next_room}")
                self.kb.remove(Atomic(f"W{x},{y}"))
                next_room.wumpus = False
                self.kb.remove(
                    Atomic(f"S{r[0]},{r[1]}")
                    for r in map.get_room(x, y).surrounding_rooms
                )

                # self.kb.add_sentence(Not(Atomic(f"W{x},{y}")))
                # self.kb.add_sentence(
                #     Not(Atomic(f"S{r[0]},{r[1]}"))
                #     for r in map.get_room(x, y).surrounding_rooms
                # )

            else:
                print(f"Nothing happened at ({x}, {y})")

    def percept(self):
        if self.current_room.wumpus or self.current_room.pit:
            self.points -= 10000
            self.alive = False
            reason = "wumpus" if self.current_room.wumpus else "pit"
            print(f"You died at {self.current_room} because of {reason}")
            return "Died"

        if (
            self.kb.check(Atomic(f"G{self.current_room.x},{self.current_room.y}"))
            == True
        ):
            self.current_room.gold = False
            self.points += 1000
            self.achieved_golds += 1
            self.kb.remove(Atomic(f"G{self.current_room.x},{self.current_room.y}"))
            return "Gold"

        special = None

        if (
            self.kb.check(Atomic(f"B{self.current_room.x},{self.current_room.y}"))
            == False
        ):  # if not breeze then cannot be pit
            for r in self.current_room.surrounding_rooms:
                self.kb.add_sentence(Not(Atomic(f"P{r[0]},{r[1]}")))
        else:
            disjunction = None
            for r in self.current_room.surrounding_rooms:
                if disjunction is None:
                    disjunction = Atomic(f"P{r[0]},{r[1]}")
                else:
                    disjunction = Or(disjunction, Atomic(f"P{r[0]},{r[1]}"))
            self.kb.add_sentence(disjunction)
            special = "Breeze"

        if (
            self.kb.check(Atomic(f"S{self.current_room.x},{self.current_room.y}"))
            == False
        ):  # if not stench then cannmot be wumpus
            for r in self.current_room.surrounding_rooms:
                self.kb.add_sentence(Not(Atomic(f"W{r[0]},{r[1]}")))
        else:
            disjunction = None
            for r in self.current_room.surrounding_rooms:
                if disjunction is None:
                    disjunction = Atomic(f"W{r[0]},{r[1]}")
                else:
                    disjunction = Or(disjunction, Atomic(f"W{r[0]},{r[1]}"))
            self.kb.add_sentence(disjunction)
            special = "Stench"

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
                if considering_room.pit == False:
                    considering_room.parent = current_room
                    self.frontier.append(considering_room)

    def find_safe(self):
        for room in self.frontier:
            if self.check_safe(room) == True:
                if room not in self.safe_rooms and room not in self.visited_rooms:
                    self.safe_rooms.append(room)

    def common_parent(self, room1, room2):
        current = room1
        current_next = room2
        current_list = [current]
        next_list = [current_next]
        while current.parent is not None and current_next.parent is not None:
            current = current.parent
            current_next = current_next.parent
            current_list.append(current)
            next_list.append(current_next)
            if current in next_list:
                return current
            if current_next in current_list:
                return current_next

        return None

    def check_safe(self, room):
        check_wumpus = Atomic(f"W{room.x},{room.y}")

        if self.kb.resolution(Not(check_wumpus)) == True:
            return True

        # if room.wumpus == False:
        #     return True

        return False

    def solve(self, moves=None, wumpus=True):
        i = 0
        if moves is None:
            moves = [(self.current_room, "Start")]
        else:
            if wumpus == False:
                moves.append((self.current_room, None))
            else:
                moves.append((self.current_room, "Shot Wumpus"))
        met_wumpus_rooms = set()

        copy_visited_rooms = []
        copy_frontier = []
        collected_golds = set()

        while self.alive:
            # if show_room:
            print(f"Current room: {self.current_room} - {self.current_room.parent}")

            i += 1
            if self.alive == False:
                break

            self.find_safe()

            next_room = None

            if len(self.safe_rooms) > 0:
                next_room = self.safe_rooms.pop(0)

            else:
                for i in range(len(self.frontier)):
                    room = self.frontier[i]
                    r = (room.x, room.y)

                    if room in self.visited_rooms:
                        continue

                    if room.wumpus == True:
                        print(str(room))
                        print([str(r[0]) for r in met_wumpus_rooms])
                        if room not in [r[0] for r in met_wumpus_rooms]:
                            met_wumpus_rooms.add(
                                (
                                    room,
                                    self.points,
                                    tuple(self.frontier.copy()),
                                    tuple(self.visited_rooms.copy()),
                                    tuple(self.kb.sentences.copy()),
                                    tuple(moves.copy()),
                                )
                            )
                        continue

                    next_room = room
                    self.frontier.pop(i)

                    self.kb.add_sentence(Not(Atomic(f"P{r[0]},{r[1]}")))
                    break

            if next_room is None:  # xong hết rồi
                copy_visited_rooms.extend(self.visited_rooms)
                copy_frontier.extend(self.frontier)  # để dùng cho locate gold

                self.exit_cave(moves)
                # print(moves[-1])
                break

            # trace đường đi

            prev = self.current_room  # phòng hiện tại (chuẩn bị là thành phòng trước)
            if next_room.parent != prev:  # trace back về
                common_parent = self.common_parent(next_room, prev)

                if common_parent is None:
                    common_parent = self.common_parent(next_room.parent, prev)

                current = prev.parent

                while True:
                    moves.append((current, None))

                    if current == common_parent:
                        break

                    prev_room = current
                    current = current.parent

                # đi từ common parent về next room
                # if founđ_initial:
                current = next_room.parent
                # else:
                #     current = copy.copy(next_room.parent.parent)

                move_back_trace = []

                while True:
                    move_back_trace.append(current)

                    if current == common_parent:
                        break

                    current = current.parent

                while len(move_back_trace) > 0:
                    current = move_back_trace.pop(-1)
                    moves.append((current, None))

            sign = self.move_to(next_room)

            special = None

            if sign == "Gold":
                collected_golds.add(next_room)
                special = "Gold"

            moves.append((next_room, special))

        if self.alive == False:
            return (-math.inf, None)

        self.visited_rooms.extend(copy_visited_rooms)
        self.frontier.extend(copy_frontier)

        for wumpus in met_wumpus_rooms:
            room, points, frontier, visited_rooms, kb, saved_moves = wumpus
            wumpus_analyse = self.analyse_wumpus(
                room, points, frontier, visited_rooms, kb, saved_moves
            )
            points = wumpus_analyse[0]
            if points > self.points and points != math.inf:
                self.points = points
                moves = wumpus_analyse[1]
                collected_golds = wumpus_analyse[2]

        return (self.points, moves, collected_golds)

    def exit_cave(self, moves):
        # search from current room to the cave
        current_room = self.current_room

        self.visited_rooms.clear()
        self.frontier.clear()
        self.safe_rooms.clear()

        self.move_to(self.current_room)
        self.find_safe()

        print("Finding cave exit...")

        while not (current_room.x == 0 and current_room.y == 0):
            # print(f"Current room: {current_room} - {current_room.parent}")
            if current_room is not None:
                self.points -= 10
            next_room = None

            shot_wumpus = False
            special = None

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

                if self.frontier[index_pop].pit == True:
                    self.frontier.pop(index_pop)
                    continue

                if self.frontier[index_pop].wumpus == True:  # chỉ nên shoot khi len = 1
                    if len(self.frontier) == 1:
                        self.shoot(self.frontier[index_pop])
                    else:
                        last_no_pit = index_pop
                        while index_pop < len(self.frontier) and (
                            self.frontier[index_pop].wumpus == True
                            or self.frontier[index_pop].pit == True
                        ):
                            if self.frontier[index_pop].pit == False:
                                last_no_pit = index_pop
                            index_pop += 1

                        if index_pop >= len(self.frontier):
                            index_pop = last_no_pit
                            self.shoot(
                                self.frontier[index_pop]
                            )  # shoot last available room
                            shot_wumpus = True

                if next_room is None:
                    next_room = self.frontier.pop(index_pop)
                else:
                    if map.heuristic(
                        self.frontier[index_pop], map.get_room(0, 0)
                    ) < map.heuristic(next_room, map.get_room(0, 0)):
                        next_room = self.frontier.pop(index_pop)

            current_room = next_room
            self.move_to(current_room)

            if shot_wumpus:
                special = "Shot Wumpus"
            # print(f"Current room: {current_room} - {current_room.parent}")
            moves.append((current_room, special))
            # print(moves[-1])

        self.points += 10  # exit cave
        print(f"Exit cave successfully")

        return current_room

    def analyse_wumpus(self, wumpus_room, points, frontier, visited_rooms, kb, moves):
        gold = self.locate_gold(wumpus_room)

        if gold == False:
            return (math.inf, None)

        new_kb = KB()
        new_kb.sentences.extend(kb)
        copy_agent = Agent(wumpus_room, new_kb)
        copy_agent.points = points

        copy_agent.frontier.extend(frontier)
        copy_agent.visited_rooms.extend(visited_rooms)

        solve = copy_agent.solve(moves=list(moves), wumpus=True)
        return solve

    def locate_gold(self, starting_room):
        frontier = []
        visited_rooms = []
        visited_rooms.extend(self.visited_rooms)
        frontier.append(starting_room)

        has_gold = False

        while len(frontier) > 0:
            current_room = frontier.pop(-1)
            visited_rooms.append(current_room)

            if current_room.gold:
                has_gold = True
                break

            for r in current_room.surrounding_rooms:
                room = map.get_room(r[0], r[1])
                if room not in visited_rooms and room not in frontier:
                    frontier.append(room)

        return has_gold


map = Map()
agent = map.random_map()
#agent = map.read_map("map5.txt")
if agent is not None:
    solve = agent.solve()
    global moves
    moves = solve[1]
    prev = None
    for room in moves:
        if room is None:
            continue
        if prev != room:
            print(f"Move to {str(room[0])} - {room[1]}")
            current = room[0]
            if agent.kb.check(Atomic(f"P{current.x},{current.y}")) == True:
                        print(f"Percept: Breeze - Possible pit at {[str(r) for r in current.surrounding_rooms]}")
            elif agent.kb.check(Atomic(f"S{current.x},{current.y}")) == True:
                        print(f"Percept: Stench - Possible wumpus at {[str(r) for r in current.surrounding_rooms]}")
            elif agent.kb.check(Not(Atomic(f"P{current.x},{current.y}"))) == True:
                        print(f"Percept: No breeze - No pit at {[str(r) for r in current.surrounding_rooms]}")
            elif agent.kb.check(Not(Atomic(f"S{current.x},{current.y}"))) == True:
                        print(f"Percept: No stench - No wumpus at {[str(r) for r in current.surrounding_rooms]}")
        prev = room
    print(f"Points: {solve[0]}")
    print(f"Collected golds: {[str(room) for room in solve[2]]}")
