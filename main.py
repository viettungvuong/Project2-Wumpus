from sympy import Function

from room import Room
from agent import Agent


agent = None

def read_map(file_name, agent):
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

map = read_map("map1.txt", agent)
