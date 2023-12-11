from room import Room

def read_map(file_name):
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

            return map


    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None

map = read_map("map1.txt")
pass
