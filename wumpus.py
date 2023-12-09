from enum import Enum


class Wumpus:
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
                self.current_room.y -= 1
        elif direction == self.Direction.BACKWARD:
            if self.current_room.y <= 9:
                self.current_room.y += 1
        elif direction == self.Direction.LEFT:
            if self.current_room.x >= 0:
                self.current_room.x -= 1
        elif direction == self.Direction.RIGHT:
            if self.current_room.x <= 9:
                self.current_room.x += 1