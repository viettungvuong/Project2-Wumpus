from enum import Enum

from room import rooms


class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    
def room_direction(current_room, direction):
    if direction == Direction.FORWARD:
        if current_room.y >= 0:
            return rooms[current_room.x][current_room.y - 1]
        else:
            return None
    elif direction == Direction.BACKWARD:
        if current_room.y <= 9:
            return rooms[current_room.x][current_room.y + 1]
        else:
            return None
    elif direction == Direction.LEFT:
        if current_room.x >= 0:
            return rooms[current_room.x - 1][current_room.y]
        else:
            return None
    elif direction == Direction.RIGHT:
        if current_room.x <= 9:
            return rooms[current_room.x + 1][current_room.y + 1]
        else:
            return None

class Agent:


    def __init__(self, current_room):
        self.current_room = current_room
        self.direction = Direction.RIGHT

    def moves(self):
        return list(Direction)

    def move(self, direction):
        next_room = room_direction(self.current_room, direction)
        if next_room is not None:
            self.current_room = next_room
        else:
            return

        if self.current_room.breeze or self.current_room.wumpus:
            print("You died!")

    def shoot(self):
        next_room = room_direction(self.current_room, self.direction)

        if next_room is not None:
            x = next_room.x
            y = next_room.y
            if rooms[x][y].wumpus:
                print("You killed the Wumpus!")
                rooms[x][y].wumpus = False
            else:
                print("You missed!")
