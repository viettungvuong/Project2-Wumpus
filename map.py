import math

from logic import Atomic
from room import Room
from agent import Agent

class Map:
    def __init__(self):
        self.map = [[Room(i, j) for j in range(10)] for i in range(10)]
        self.gold = []
        self.n = 0

    def gold_heuristic(self, current_room, goal_room):
        return math.sqrt((current_room.x - goal_room.x) ** 2 + (current_room.y - goal_room.y) ** 2)
        # euclidean distance

    def read_map(self, file_name, agent):
        try:
            with open(file_name, 'r') as lines:
                n = int(lines.readline())
                self.n = n

                # 2d array representing the map
                map = [[Room(i, j) for j in range(n)] for i in range(n)]

                for i in range(n):
                    line = lines.readline()
                    line_split = line.split('.')
                    for j in range(n):
                        if line_split[j].__contains__("A"):
                            agent = Agent(map[i][j])

                        elif line_split[j].__contains__("G"):
                            self.gold.append(map[i][j])
                            agent.kb.add_sentence(Atomic(f"G{map[i][j].x},{map[i][j].y}"))

                        elif line_split[j].__contains__("W"): # meet wumpus
                            agent.kb.add_sentence(Atomic(f"W{map[i][j].x},{map[i][j].y}"))
                            moves = map[i][j].surrounding_rooms
                            for move in moves:
                                agent.kb.add_sentence(Atomic(f"S{move[0]},{move[1]}"))

                        elif line_split[j].__contains__("P"):
                            agent.kb.add_sentence(Atomic(f"P{map[i][j].x},{map[i][j].y}"))
                            moves = map[i][j].surrounding_rooms
                            for move in moves:
                                agent.kb.add_sentence(Atomic(f"B{move[0]},{move[1]}"))

                return map


        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
            return None