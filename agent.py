from enum import Enum

from room import rooms


class Agent:
    class Direction(Enum):
        FORWARD = 1
        BACKWARD = 2
        LEFT = 3
        RIGHT = 4

    def __init__(self, current_room):
        self.current_room = current_room
        self.direction = self.Direction.RIGHT

    def moves(self):
        return list(self.Direction)

    def move(self, direction):
        if direction == self.Direction.FORWARD:
            if self.current_room.y >= 0:
                self.current_room = rooms[self.current_room.x][self.current_room.y - 1]
            else:
                return
        elif direction == self.Direction.BACKWARD:
            if self.current_room.y <= 9:
                self.current_room = rooms[self.current_room.x][self.current_room.y + 1]
            else:
                return
        elif direction == self.Direction.LEFT:
            if self.current_room.x >= 0:
                self.current_room = rooms[self.current_room.x - 1][self.current_room.y]
            else:
                return
        elif direction == self.Direction.RIGHT:
            if self.current_room.x <= 9:
                self.current_room = rooms[self.current_room.x + 1][self.current_room.y + 1]
            else:
                return

        if self.current_room.breeze or self.current_room.wumpus:
            print("You died!")

