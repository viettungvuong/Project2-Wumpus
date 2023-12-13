import math

from sympy import Function

from room import Room
from agent import Agent


agent = None

class Map:
    def __init__(self):
        self.map = [[Room(i, j) for j in range(10)] for i in range(10)]
        self.gold = []

    def gold_heuristic(current_room, room):
        return math.sqrt((current_room.x - room.x) ** 2 + (current_room.y - room.y) ** 2)
        # euclidean distance

    def read_map(self, file_name, agent):
        try:
            with open(file_name, 'r') as lines:
                n = int(lines.readline())

                # 2d array representing the map
                map = [[Room(i, j) for j in range(n)] for i in range(n)]

                for i in range(n):
                    line = lines.readline()
                    line_split = line.split('.')
                    for j in range(n):
                        map[i][j].set_room(line_split[j])

                        if line_split[j].__contains__("A"):
                            agent = Agent(map[i][j])
                        elif line_split[j].__contains__("G"):
                            self.gold.append(map[i][j])
                        elif line_split[j].__contains__("W"):
                            moves = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                            for move in moves:
                                if move[0] >= 0 and move[0] < n and move[1] >= 0 and move[1] < n:
                                    map[move[0]][move[1]].set_room("S")
                        elif line_split[j].__contains__("P"):
                            moves = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                            for move in moves:
                                if move[0] >= 0 and move[0] < n and move[1] >= 0 and move[1] < n:
                                    map[move[0]][move[1]].set_room("B")

                return map


        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
            return None

map = Map()
map.read_map("map.txt", agent)
